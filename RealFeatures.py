"""Realistic, typed node features for VirtualSoc.

The original simulation generates *abstract* features: plain numbers drawn
from a numpy distribution, compared with an absolute difference inside the
sDNA score (Node.getScore / getScoreAdvanced). That is fine for benchmark
graphs, but real social-network attributes are not all numeric: the
"distance" between two cities is not |5 - 95|, and two users' interest
sets need overlap, not subtraction.

This module adds typed features with type-aware dissimilarities while
keeping the sDNA machinery (per-feature preference l in {-1, +1} and
weight w in [0, 1], mutation, labels) exactly as in the paper
(arXiv:1905.09087, Eq. 1-2):

    feature score(i -> j) = sum_k  d_k(f_ik, f_jk) * w_k * l_k

where d_k is a dissimilarity in [0, 1] appropriate to the feature type:

    numeric      |a - b| / range          (age, ordinal education, ...)
    binary       0 if equal else 1        (gender as 0/1)
    categorical  0 if equal else 1        (city, occupation, ...)
    geo          euclidean / diagonal     ((x, y) coordinates)
    multihot     1 - Jaccard overlap      (interest sets)

l = -1 preserves the original semantics: the node prefers *similar*
values (larger difference lowers the score); l = +1 prefers dissimilar.

Nodes built from a schema also carry a numeric encoding of their typed
features (normalised numerics, one-hot categoricals, 0/1 interest
vectors) in the standard ``Node.features`` list, so everything downstream
(saving, GCN training on the exported feature matrix) works unchanged.

Quick start::

    from RealFeatures import RealFeatureSchema
    from Networks import RandomSocialGraphAdvanced

    schema = RealFeatureSchema.default_social()
    G = RandomSocialGraphAdvanced(labelSplit=[25, 50, 75, 100],
                                  realFeatureSchema=schema,
                                  useGPU=False, createInGPUMem=False,
                                  ...)
"""

import numpy as np

from Node import NodeSocial


# ------------------------------------------------------------- samplers --
# A sampler is callable(size, rng) -> sequence of values. These defaults
# mimic realistic marginal distributions; pass your own for other shapes.


def age_sampler(size, rng):
    """Platform-like age mixture, skewed young, clipped to [13, 90]."""
    comp = rng.choice(4, size=size, p=[0.35, 0.30, 0.20, 0.15])
    means = np.array([23.0, 32.0, 45.0, 62.0])[comp]
    sds = np.array([4.0, 6.0, 8.0, 10.0])[comp]
    return np.clip(rng.normal(means, sds), 13, 90).round().astype(int)


def binary_sampler(p_one=0.49):
    def sample(size, rng):
        return (rng.random(size) < p_one).astype(int)
    return sample


def zipf_categorical_sampler(n_categories, s=1.2):
    """Categories with Zipf-like popularity (a few big cities, many small)."""
    w = 1.0 / np.arange(1, n_categories + 1) ** s
    w /= w.sum()

    def sample(size, rng):
        return rng.choice(n_categories, size=size, p=w)
    return sample


def ordinal_sampler(probabilities):
    probabilities = np.asarray(probabilities, dtype=float)
    probabilities /= probabilities.sum()

    def sample(size, rng):
        return rng.choice(len(probabilities), size=size, p=probabilities)
    return sample


def geo_sampler(n_centres=30, spread=0.03, s=1.2):
    """(x, y) positions clustered around population-weighted centres."""
    def sample(size, rng):
        centres = rng.random((n_centres, 2))
        w = 1.0 / np.arange(1, n_centres + 1) ** s
        w /= w.sum()
        idx = rng.choice(n_centres, size=size, p=w)
        pts = np.clip(centres[idx] + rng.normal(0, spread, (size, 2)), 0, 1)
        return [tuple(p) for p in pts]
    return sample


def multihot_sampler(n_items=20, mean_k=3.0):
    """Interest sets: 1 + Poisson(mean_k - 1) topics out of n_items."""
    def sample(size, rng):
        out = []
        for _ in range(size):
            k = min(n_items, 1 + rng.poisson(max(mean_k - 1.0, 0.0)))
            out.append(frozenset(rng.choice(n_items, size=k, replace=False).tolist()))
        return out
    return sample


# ----------------------------------------------------------------- spec --


class FeatureSpec:
    """One typed feature: a name, a kind, a sampler, and kind parameters."""

    KINDS = ("numeric", "binary", "categorical", "geo", "multihot")

    def __init__(self, name, kind, sampler, value_range=None,
                 n_categories=None, n_items=None):
        if kind not in self.KINDS:
            raise ValueError(f"unknown feature kind {kind!r}; expected one of {self.KINDS}")
        if kind == "numeric" and value_range is None:
            raise ValueError(f"numeric feature {name!r} needs value_range=(lo, hi)")
        if kind == "categorical" and n_categories is None:
            raise ValueError(f"categorical feature {name!r} needs n_categories")
        if kind == "multihot" and n_items is None:
            raise ValueError(f"multihot feature {name!r} needs n_items")
        self.name = name
        self.kind = kind
        self.sampler = sampler
        self.value_range = value_range
        self.n_categories = n_categories
        self.n_items = n_items

    def sample(self, size, rng):
        return self.sampler(size, rng)

    def dissimilarity(self, a, b):
        """Type-aware dissimilarity in [0, 1]."""
        if self.kind == "numeric":
            lo, hi = self.value_range
            return abs(float(a) - float(b)) / max(hi - lo, 1e-12)
        if self.kind in ("binary", "categorical"):
            return 0.0 if a == b else 1.0
        if self.kind == "geo":
            dx, dy = a[0] - b[0], a[1] - b[1]
            return float(np.hypot(dx, dy)) / np.sqrt(2.0)
        # multihot
        union = a | b
        if not union:
            return 0.0
        return 1.0 - len(a & b) / len(union)

    def encoded_length(self):
        if self.kind == "categorical":
            return self.n_categories
        if self.kind == "geo":
            return 2
        if self.kind == "multihot":
            return self.n_items
        return 1

    def encode(self, value):
        """Numeric encoding for export / GCN training."""
        if self.kind == "numeric":
            lo, hi = self.value_range
            return [(float(value) - lo) / max(hi - lo, 1e-12)]
        if self.kind == "binary":
            return [float(value)]
        if self.kind == "categorical":
            out = [0.0] * self.n_categories
            out[int(value)] = 1.0
            return out
        if self.kind == "geo":
            return [float(value[0]), float(value[1])]
        return [1.0 if i in value else 0.0 for i in range(self.n_items)]


# --------------------------------------------------------------- schema --


class RealFeatureSchema:
    """An ordered collection of FeatureSpec defining a node's attributes.

    The sDNA length must equal ``len(schema.specs)`` (one preference and
    one weight per typed feature), which the factory below handles.
    """

    def __init__(self, specs):
        if not specs:
            raise ValueError("schema needs at least one FeatureSpec")
        self.specs = list(specs)

    @property
    def n_features(self):
        return len(self.specs)

    def sample(self, n, seed=None):
        """Sample features for n nodes -> list of per-node value lists."""
        rng = np.random.default_rng(seed)
        columns = [spec.sample(n, rng) for spec in self.specs]
        return [[col[i] for col in columns] for i in range(n)]

    def dissimilarity_vector(self, values_a, values_b):
        return np.array([spec.dissimilarity(a, b) for spec, a, b
                         in zip(self.specs, values_a, values_b)])

    def encode(self, values):
        """Flat numeric vector (for Node.features / GCN export)."""
        out = []
        for spec, v in zip(self.specs, values):
            out.extend(spec.encode(v))
        return out

    def encoded_feature_names(self):
        names = []
        for spec in self.specs:
            n = spec.encoded_length()
            if n == 1:
                names.append(spec.name)
            elif spec.kind == "geo":
                names.extend([f"{spec.name}_x", f"{spec.name}_y"])
            else:
                names.extend([f"{spec.name}_{i}" for i in range(n)])
        return names

    @classmethod
    def default_social(cls, n_cities=30, n_topics=20):
        """Age, gender, city, geo position, education, interests."""
        return cls([
            FeatureSpec("age", "numeric", age_sampler, value_range=(13, 90)),
            FeatureSpec("gender", "binary", binary_sampler(0.49)),
            FeatureSpec("city", "categorical",
                        zipf_categorical_sampler(n_cities), n_categories=n_cities),
            FeatureSpec("geo", "geo", geo_sampler()),
            FeatureSpec("education", "numeric",
                        ordinal_sampler([0.10, 0.25, 0.30, 0.25, 0.10]),
                        value_range=(0, 4)),
            FeatureSpec("interests", "multihot",
                        multihot_sampler(n_topics), n_items=n_topics),
        ])


# ----------------------------------------------------------------- node --


class NodeSocialReal(NodeSocial):
    """NodeSocial with typed features and type-aware sDNA scoring.

    ``Node.features`` still holds the flat numeric encoding (so exports and
    downstream GCN training are unchanged); the typed values used for
    scoring live in ``featureValues``.
    """

    def __init__(self, label, DNA, Graph, schema, featureValues):
        self.schema = schema
        self.featureValues = list(featureValues)
        super().__init__(label=label, DNA=DNA, Graph=Graph,
                         additionalFeatures=schema.encode(featureValues))

    def getScore(self, other):
        """Paper Eq. 1 with type-aware dissimilarities (self's sDNA only;
        the socialiser adds both directions per Eq. 2)."""
        d = self.schema.dissimilarity_vector(self.featureValues,
                                             other.featureValues)
        w = np.asarray(self.DNA.value[1::2], dtype=float)
        p = np.asarray(self.DNA.value[0::2], dtype=float)
        return float(np.sum(d * w * p))

    def getScoreAdvanced(self, other, popularityPreferenceIntensity,
                         mutualPreferenceIntensity,
                         multPopularityPreference=False,
                         multMutualPreference=False):
        """Typed feature score plus the popularity and path-length terms,
        with identical semantics to NodeSocial.getScoreAdvanced."""
        sumScore = self.getScore(other)

        if multPopularityPreference:
            sumScore = sumScore * popularityPreferenceIntensity * (other.outDegree + other.inDegree)
        else:
            sumScore = sumScore + popularityPreferenceIntensity * (other.outDegree + other.inDegree) * self.DNA.preferPopularityIntensity

        if self.Graph.Socialised:
            if mutualPreferenceIntensity is not None:
                i = 0
                tempPath2 = 0
                tempPath3 = 0
                tempPath4 = 0
                for mpi in mutualPreferenceIntensity:
                    if i == 0:
                        if self.Graph.adjP2[self.ID, other.ID] > 0:
                            tempPath2 = mpi * self.DNA.preferShorterPathIntensity[0]
                    elif i == 1:
                        if self.Graph.adjP3[self.ID, other.ID] > 0:
                            tempPath3 = mpi * self.DNA.preferShorterPathIntensity[1]
                    elif i == 2:
                        if self.Graph.adjP4[self.ID, other.ID] > 0:
                            tempPath4 = mpi * self.DNA.preferShorterPathIntensity[2]
                    i += 1
                if multMutualPreference:
                    if tempPath2 != 0:
                        sumScore = sumScore * tempPath2
                    if tempPath3 != 0:
                        sumScore = sumScore * tempPath3
                    if tempPath4 != 0:
                        sumScore = sumScore * tempPath4
                else:
                    # additive path-length preference (paper Eq. 9)
                    sumScore = sumScore + tempPath2 + tempPath3 + tempPath4

        return sumScore


# -------------------------------------------------------------- factory --


def createSocialNodesRealFeatures(Graph, labelSplit, schema, DnaObjType,
                                  dna='auto', shuffledDNA=True, seed=None):
    """Generate NodeSocialReal nodes from a RealFeatureSchema.

    Mirrors PetriDish.createSocialNodesNFeaturesSameDistWithDNAShuffled:
    one sDNA (and label) per entry of ``labelSplit``, node labels shuffled
    across the population when ``shuffledDNA`` is True. The sDNA length is
    ``schema.n_features`` (one preference/weight pair per typed feature).
    """
    numberOfNodes = labelSplit[-1]
    values = schema.sample(numberOfNodes, seed=seed)

    DNAlist = [DnaObjType(dna, len=schema.n_features, useGPU=Graph._useGPU,
                          createInGPUMem=False)
               for _ in range(len(labelSplit))]

    spread = np.empty(numberOfNodes, dtype=int)
    start = 0
    for i in range(len(labelSplit)):
        spread[start:labelSplit[i]] = i
        start = labelSplit[i]
    if shuffledDNA:
        rng = np.random.default_rng(seed)
        rng.shuffle(spread)

    N = []
    for j in range(numberOfNodes):
        label = int(spread[j])
        node = NodeSocialReal(label=label, DNA=DNAlist[label], Graph=Graph,
                              schema=schema, featureValues=values[j])
        DNAlist[label]._assignedNode(node)
        N.append(node)

    Graph.DNA = DNAlist
    return N
