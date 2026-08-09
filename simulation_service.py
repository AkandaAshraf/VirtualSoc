"""Simulation service for the VirtualSoc web API.

Turns a validated JSON request into a simulated dynamic social network
(via RandomSocialGraphAdvanced + RealFeatureSchema), tracked as an
asynchronous job with progress reporting, and packages the results
(per-snapshot edge lists, ground-truth labels, typed and GCN-ready
encoded features, summary statistics) for download.

Security note: unlike the library's legacy ``npDistFunc`` strings (which
are eval'd), this service builds feature schemas from validated JSON
only -- nothing user-supplied is ever executed.
"""

import csv
import io
import json
import threading
import time
import uuid
import zipfile

import numpy as np

from Networks import RandomSocialGraphAdvanced
from RealFeatures import (FeatureSpec, RealFeatureSchema, age_sampler,
                          binary_sampler, geo_sampler, multihot_sampler,
                          ordinal_sampler, zipf_categorical_sampler)

LIMITS = {
    "n_people": (10, 2000),
    "n_groups": (2, 10),
    "time_steps": (1, 10),
    "n_attributes": (1, 30),
}


# ------------------------------------------------------- schema building --


def _uniform_int_sampler(low, high):
    def sample(size, rng):
        return rng.integers(low, high + 1, size=size)
    return sample


def _uniform_sampler(low, high):
    def sample(size, rng):
        return rng.uniform(low, high, size=size)
    return sample


def _normal_sampler(mean, sd, low, high):
    def sample(size, rng):
        return np.clip(rng.normal(mean, sd, size=size), low, high)
    return sample


def build_schema(attributes):
    """Build a RealFeatureSchema from the validated JSON description.

    ``attributes`` is either {"preset": "default_social"} or
    {"specs": [{...}, ...]} -- see spec_from_json for the spec format.
    """
    if not isinstance(attributes, dict):
        raise ValueError("attributes must be an object")
    if attributes.get("preset") == "default_social":
        return RealFeatureSchema.default_social()
    specs = attributes.get("specs")
    if not specs:
        raise ValueError("attributes needs a 'preset' or a non-empty 'specs' list")
    lo, hi = LIMITS["n_attributes"]
    if not lo <= len(specs) <= hi:
        raise ValueError(f"number of attributes must be within {lo}..{hi}")
    return RealFeatureSchema([spec_from_json(s, i) for i, s in enumerate(specs)])


def spec_from_json(s, index):
    name = str(s.get("name") or f"feature_{index}")[:40]
    kind = s.get("kind")
    if kind == "numeric":
        preset = s.get("preset")
        if preset == "age":
            return FeatureSpec(name, "numeric", age_sampler, value_range=(13, 90))
        low = float(s.get("low", 0.0))
        high = float(s.get("high", 1.0))
        if not high > low:
            raise ValueError(f"{name}: numeric needs high > low")
        if s.get("distribution") == "normal":
            mean = float(s.get("mean", (low + high) / 2))
            sd = float(s.get("sd", (high - low) / 6 or 1.0))
            sampler = _normal_sampler(mean, sd, low, high)
        elif s.get("integer", True):
            sampler = _uniform_int_sampler(int(low), int(high))
        else:
            sampler = _uniform_sampler(low, high)
        return FeatureSpec(name, "numeric", sampler, value_range=(low, high))
    if kind == "ordinal":
        probs = s.get("probabilities") or [1.0] * int(s.get("levels", 5))
        return FeatureSpec(name, "numeric", ordinal_sampler(probs),
                           value_range=(0, len(probs) - 1))
    if kind == "binary":
        return FeatureSpec(name, "binary",
                           binary_sampler(float(s.get("p_one", 0.5))))
    if kind == "categorical":
        n = int(s.get("n_categories", 10))
        if not 2 <= n <= 1000:
            raise ValueError(f"{name}: n_categories must be within 2..1000")
        return FeatureSpec(name, "categorical",
                           zipf_categorical_sampler(n, float(s.get("zipf_s", 1.2))),
                           n_categories=n)
    if kind == "geo":
        return FeatureSpec(name, "geo",
                           geo_sampler(n_centres=int(s.get("n_centres", 30))))
    if kind == "multihot":
        n = int(s.get("n_items", 20))
        if not 2 <= n <= 500:
            raise ValueError(f"{name}: n_items must be within 2..500")
        return FeatureSpec(name, "multihot",
                           multihot_sampler(n, float(s.get("mean_k", 3.0))),
                           n_items=n)
    raise ValueError(f"{name}: unknown kind {kind!r}; expected numeric, "
                     "ordinal, binary, categorical, geo or multihot")


# ------------------------------------------------------------ validation --


def validate_request(body):
    """Validate/normalise a /api/simulate request body -> params dict."""
    if not isinstance(body, dict):
        raise ValueError("request body must be a JSON object")

    def clamped(key, default, cast=int):
        lo, hi = LIMITS[key]
        v = cast(body.get(key, default))
        if not lo <= v <= hi:
            raise ValueError(f"{key} must be within {lo}..{hi}")
        return v

    n_people = clamped("n_people", 200)
    n_groups = clamped("n_groups", 4)
    time_steps = clamped("time_steps", 3)
    split = np.linspace(n_people / n_groups, n_people, n_groups).round().astype(int)
    params = {
        "n_people": n_people,
        "n_groups": n_groups,
        "label_split": split.tolist(),
        "time_steps": time_steps,
        "mutation_intensity": float(body.get("mutation_intensity", 0.01)),
        "exploration_probability": float(body.get("exploration_probability", 0.3)),
        "connection_percentage": float(body.get("connection_percentage", 5)),
        "popularity_preference": float(body.get("popularity_preference", 0.5)),
        "path_preference": [float(x) for x in
                            (body.get("path_preference") or [0.9, 0.3, 0.1])[:3]],
        "attributes": body.get("attributes") or {"preset": "default_social"},
        "seed": int(body["seed"]) if body.get("seed") is not None else None,
    }
    if not 0.0 < params["exploration_probability"] <= 1.0:
        raise ValueError("exploration_probability must be in (0, 1]")
    if not 0.0 < params["connection_percentage"] <= 100.0:
        raise ValueError("connection_percentage must be in (0, 100]")
    if not 0.0 <= params["mutation_intensity"] <= 1.0:
        raise ValueError("mutation_intensity must be in [0, 1]")
    if len(params["path_preference"]) != 3:
        raise ValueError("path_preference needs three values (2-, 3-, 4-paths)")
    build_schema(params["attributes"])  # validate attributes early
    return params


# -------------------------------------------------------------- the run --


def _edge_set(G):
    return {(min(i, j), max(i, j)) for (i, j) in G.adjMatDict
            if G.adjMatDict[i, j] is not None}


def _json_safe(value):
    if isinstance(value, frozenset):
        return sorted(int(x) for x in value)
    if isinstance(value, tuple):
        return [round(float(x), 6) for x in value]
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return round(float(value), 6)
    return value


def _snapshot_stats(G, edges, prev_edges, schema):
    n = G.nodeCount
    stats = {
        "nodes": n,
        "edges": len(edges),
        "new_edges": len(edges - prev_edges) if prev_edges is not None else len(edges),
        "density": round(2 * len(edges) / (n * (n - 1)), 6),
        "mean_degree": round(2 * len(edges) / n, 3),
    }
    homophily = {}
    for ix, spec in enumerate(schema.specs):
        if spec.kind in ("binary", "categorical") and edges:
            same = sum(1 for (i, j) in edges
                       if G.N[i].featureValues[ix] == G.N[j].featureValues[ix])
            homophily[spec.name] = round(same / len(edges), 4)
    if homophily:
        stats["homophily"] = homophily
    return stats


def run_simulation(params, progress=lambda pct, msg: None):
    """Run the simulation; returns the full result dict."""
    schema = build_schema(params["attributes"])
    t0 = time.perf_counter()
    steps = params["time_steps"]

    progress(2, "creating population")
    G = RandomSocialGraphAdvanced(
        labelSplit=params["label_split"],
        realFeatureSchema=schema,
        realFeatureSeed=params["seed"],
        explorationProbability=params["exploration_probability"],
        connectionPercentageWithMatchedNodes=params["connection_percentage"],
        popularityPreferenceIntensity=params["popularity_preference"],
        mutualPreferenceIntensity=params["path_preference"],
        useGPU=False, createInGPUMem=False,
        keepHistory=False, numberofProcesses=None,
        socialiseOnCreation=False)

    snapshots = []
    prev = None
    for t in range(steps):
        progress(5 + int(90 * t / steps), f"socialising snapshot {t + 1}/{steps}")
        if t > 0:
            G.mutateDNA(mutationIntensity=params["mutation_intensity"],
                        mutatePreference=True, mutatePreferenceProbability=True)
        G.socialise()
        edges = _edge_set(G)
        snapshots.append({
            "t": t,
            "edges": sorted(edges),
            "stats": _snapshot_stats(G, edges, prev, schema),
        })
        prev = edges

    progress(97, "packaging results")
    result = {
        "params": params,
        "schema": [{"name": s.name, "kind": s.kind} for s in schema.specs],
        "encoded_feature_names": schema.encoded_feature_names(),
        "nodes": [{
            "id": node.ID,
            "label": int(node.label),
            "values": [_json_safe(v) for v in node.featureValues],
            "encoded": [round(float(x), 6) for x in node.features],
        } for node in G.N],
        "snapshots": [{"t": s["t"], "stats": s["stats"],
                       "n_edges": len(s["edges"])} for s in snapshots],
        "edges_by_snapshot": {str(s["t"]): [list(e) for e in s["edges"]]
                              for s in snapshots},
        "elapsed_seconds": round(time.perf_counter() - t0, 2),
    }
    progress(100, "done")
    return result


def result_zip(result):
    """Bundle a result dict into an in-memory zip of CSV/JSON files."""
    buf = io.BytesIO()

    def write_csv(z, name, header, rows):
        s = io.StringIO()
        w = csv.writer(s)
        w.writerow(header)
        w.writerows(rows)
        z.writestr(name, s.getvalue())

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("params.json", json.dumps(result["params"], indent=1))
        z.writestr("schema.json", json.dumps({
            "attributes": result["schema"],
            "encoded_feature_names": result["encoded_feature_names"]}, indent=1))
        write_csv(z, "labels.csv", ["node_id", "label"],
                  [(n["id"], n["label"]) for n in result["nodes"]])
        write_csv(z, "features_encoded.csv",
                  ["node_id"] + result["encoded_feature_names"],
                  [[n["id"]] + n["encoded"] for n in result["nodes"]])
        z.writestr("features_typed.json", json.dumps(
            [{"id": n["id"], **dict(zip([a["name"] for a in result["schema"]],
                                        n["values"]))}
             for n in result["nodes"]], indent=1))
        for t, edges in result["edges_by_snapshot"].items():
            write_csv(z, f"edges_t{t}.csv", ["source", "target"], edges)
        z.writestr("stats.json", json.dumps(result["snapshots"], indent=1))
        z.writestr("README.txt",
                   "VirtualSoc simulated social network\n"
                   "===================================\n"
                   "labels.csv            ground-truth node labels (sDNA groups)\n"
                   "features_encoded.csv  numeric feature matrix (GCN-ready)\n"
                   "features_typed.json   typed attribute values per node\n"
                   "edges_t{K}.csv        undirected edge list of snapshot K\n"
                   "stats.json            per-snapshot statistics\n"
                   "Generated by the VirtualSoc simulation suite\n"
                   "(arXiv:1905.09087). Simulated data: contains no real\n"
                   "individuals, safe to share.\n")
    buf.seek(0)
    return buf


# ------------------------------------------------------------- job store --


class JobStore:
    """Small in-memory job manager running simulations in worker threads."""

    MAX_JOBS = 50

    def __init__(self):
        self._jobs = {}
        self._lock = threading.Lock()

    def submit(self, params):
        job_id = uuid.uuid4().hex[:12]
        with self._lock:
            while len(self._jobs) >= self.MAX_JOBS:
                oldest = min(self._jobs, key=lambda k: self._jobs[k]["created"])
                del self._jobs[oldest]
            self._jobs[job_id] = {
                "status": "queued", "progress": 0, "message": "queued",
                "created": time.time(), "params": params,
                "result": None, "error": None,
            }
        threading.Thread(target=self._run, args=(job_id,), daemon=True).start()
        return job_id

    def _run(self, job_id):
        def progress(pct, msg):
            with self._lock:
                if job_id in self._jobs:
                    self._jobs[job_id].update(progress=pct, message=msg,
                                              status="running")
        try:
            result = run_simulation(self.get(job_id)["params"], progress)
            with self._lock:
                if job_id in self._jobs:
                    self._jobs[job_id].update(status="done", progress=100,
                                              message="done", result=result)
        except Exception as exc:  # surfaced via the API, not swallowed
            with self._lock:
                if job_id in self._jobs:
                    self._jobs[job_id].update(status="error",
                                              message=f"{type(exc).__name__}: {exc}",
                                              error=str(exc))

    def get(self, job_id):
        with self._lock:
            job = self._jobs.get(job_id)
            return dict(job) if job else None

    def public_view(self, job_id):
        job = self.get(job_id)
        if job is None:
            return None
        return {"job_id": job_id, "status": job["status"],
                "progress": job["progress"], "message": job["message"]}
