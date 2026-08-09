"""VirtualSoc simulation suite -- Flask web API + built-in UI.

Lets researchers generate privacy-safe simulated social networks (with
ground-truth labels, typed features and dynamic snapshots) to test their
algorithms and theories without accessing real social networks -- the
purpose set out in the paper (arXiv:1905.09087, Section 1).

Run:
    python webapp.py            # http://127.0.0.1:5000

API:
    GET  /api/limits                    parameter limits + feature kinds
    POST /api/simulate                  start a simulation -> {job_id}
    GET  /api/jobs/<id>                 progress {status, progress, message}
    GET  /api/jobs/<id>/result          full result JSON
    GET  /api/jobs/<id>/download        zip: edge lists per snapshot,
                                        labels, typed + encoded features,
                                        statistics

Example request body for POST /api/simulate:
    {
      "n_people": 200, "n_groups": 4, "time_steps": 3,
      "mutation_intensity": 0.01, "exploration_probability": 0.3,
      "connection_percentage": 5, "popularity_preference": 0.5,
      "path_preference": [0.9, 0.3, 0.1], "seed": 42,
      "attributes": {"preset": "default_social"}
    }
or with custom attributes:
    "attributes": {"specs": [
      {"name": "age", "kind": "numeric", "preset": "age"},
      {"name": "gender", "kind": "binary", "p_one": 0.49},
      {"name": "city", "kind": "categorical", "n_categories": 30},
      {"name": "interests", "kind": "multihot", "n_items": 20}
    ]}
"""

from flask import Flask, jsonify, render_template, request, send_file

from simulation_service import LIMITS, JobStore, result_zip, validate_request

app = Flask(__name__)
jobs = JobStore()


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/limits")
def limits():
    return jsonify({
        "limits": {k: {"min": lo, "max": hi} for k, (lo, hi) in LIMITS.items()},
        "feature_kinds": ["numeric", "ordinal", "binary", "categorical",
                          "geo", "multihot"],
        "presets": ["default_social"],
    })


@app.post("/api/simulate")
def simulate():
    try:
        params = validate_request(request.get_json(force=True, silent=False))
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400
    job_id = jobs.submit(params)
    return jsonify({"job_id": job_id}), 202


@app.get("/api/jobs/<job_id>")
def job_status(job_id):
    view = jobs.public_view(job_id)
    if view is None:
        return jsonify({"error": "unknown job"}), 404
    return jsonify(view)


@app.get("/api/jobs/<job_id>/result")
def job_result(job_id):
    job = jobs.get(job_id)
    if job is None:
        return jsonify({"error": "unknown job"}), 404
    if job["status"] != "done":
        return jsonify({"error": f"job is {job['status']}"}), 409
    return jsonify(job["result"])


@app.get("/api/jobs/<job_id>/download")
def job_download(job_id):
    job = jobs.get(job_id)
    if job is None:
        return jsonify({"error": "unknown job"}), 404
    if job["status"] != "done":
        return jsonify({"error": f"job is {job['status']}"}), 409
    return send_file(result_zip(job["result"]), mimetype="application/zip",
                     as_attachment=True,
                     download_name=f"virtualsoc_{job_id}.zip")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, threaded=True)
