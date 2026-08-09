import numpy as np
import pytest

from DNA import DNAadvanced
from RealFeatures import (FeatureSpec, NodeSocialReal, RealFeatureSchema,
                          age_sampler, binary_sampler,
                          createSocialNodesRealFeatures, geo_sampler,
                          multihot_sampler, zipf_categorical_sampler)
from Networks import RandomSocialGraphAdvanced


def make_graph_shell():
    """A minimal Graph-like container for constructing nodes directly."""
    from Networks import Graph

    g = Graph()
    g._useGPU = False
    g.createInGPUMem = False
    g.Socialised = False
    return g


# ---------------------------------------------------------------- schema --


def test_default_schema_samples_shapes_and_types():
    schema = RealFeatureSchema.default_social(n_cities=10, n_topics=8)
    vals = schema.sample(50, seed=1)
    assert len(vals) == 50 and all(len(v) == schema.n_features for v in vals)
    ages = [v[0] for v in vals]
    assert all(13 <= a <= 90 for a in ages)
    assert set(v[1] for v in vals) <= {0, 1}
    assert all(0 <= v[2] < 10 for v in vals)
    assert all(0.0 <= v[3][0] <= 1.0 and 0.0 <= v[3][1] <= 1.0 for v in vals)
    assert all(0 <= v[4] <= 4 for v in vals)
    assert all(isinstance(v[5], frozenset) and len(v[5]) >= 1 for v in vals)


def test_sampling_is_reproducible_with_seed():
    schema = RealFeatureSchema.default_social()
    assert schema.sample(20, seed=7) == schema.sample(20, seed=7)


def test_dissimilarities_are_normalised_and_symmetric():
    schema = RealFeatureSchema.default_social(n_cities=5, n_topics=6)
    a, b = schema.sample(2, seed=3)
    d_ab = schema.dissimilarity_vector(a, b)
    d_ba = schema.dissimilarity_vector(b, a)
    assert np.allclose(d_ab, d_ba)
    assert np.all(d_ab >= 0.0) and np.all(d_ab <= 1.0)
    assert np.allclose(schema.dissimilarity_vector(a, a), 0.0)


def test_typed_dissimilarity_semantics():
    num = FeatureSpec("age", "numeric", age_sampler, value_range=(0, 100))
    assert num.dissimilarity(20, 70) == pytest.approx(0.5)
    cat = FeatureSpec("city", "categorical",
                      zipf_categorical_sampler(9), n_categories=9)
    assert cat.dissimilarity(3, 3) == 0.0 and cat.dissimilarity(3, 4) == 1.0
    geo = FeatureSpec("geo", "geo", geo_sampler())
    assert geo.dissimilarity((0, 0), (1, 1)) == pytest.approx(1.0)
    mh = FeatureSpec("ints", "multihot", multihot_sampler(6), n_items=6)
    assert mh.dissimilarity(frozenset({1, 2}), frozenset({2, 3})) == pytest.approx(2 / 3)
    assert mh.dissimilarity(frozenset(), frozenset()) == 0.0


def test_encoding_shapes_and_names():
    schema = RealFeatureSchema.default_social(n_cities=4, n_topics=5)
    vals = schema.sample(3, seed=0)
    enc = schema.encode(vals[0])
    expected = 1 + 1 + 4 + 2 + 1 + 5
    assert len(enc) == expected
    assert len(schema.encoded_feature_names()) == expected
    city_onehot = enc[2:6]
    assert sum(city_onehot) == 1.0


# ----------------------------------------------------------------- node --


def test_typed_scoring_prefers_similar_when_preference_is_minus_one():
    schema = RealFeatureSchema([
        FeatureSpec("age", "numeric", age_sampler, value_range=(0, 100)),
    ])
    g = make_graph_shell()
    # preference -1 (prefer similar), weight 1.0
    dna = DNAadvanced([-1, 1.0], len=1, useGPU=False, createInGPUMem=False)
    dna.preferPopularityIntensity = 0.0
    dna.preferShorterPathIntensity = [0, 0, 0]
    me = NodeSocialReal(label=0, DNA=dna, Graph=g, schema=schema, featureValues=[30])
    close = NodeSocialReal(label=0, DNA=dna, Graph=g, schema=schema, featureValues=[35])
    far = NodeSocialReal(label=0, DNA=dna, Graph=g, schema=schema, featureValues=[80])
    assert me.getScore(close) > me.getScore(far)
    # flip preference to +1 (prefer dissimilar) and the order reverses
    dna.value[0] = 1
    assert me.getScore(close) < me.getScore(far)


def test_encoded_features_available_for_export():
    schema = RealFeatureSchema.default_social(n_cities=6, n_topics=4)
    g = make_graph_shell()
    dna = DNAadvanced('auto', len=schema.n_features, useGPU=False,
                      createInGPUMem=False)
    node = NodeSocialReal(label=0, DNA=dna, Graph=g, schema=schema,
                          featureValues=schema.sample(1, seed=5)[0])
    assert len(node.features) == 1 + 1 + 6 + 2 + 1 + 4
    assert all(isinstance(x, float) for x in node.features)


# -------------------------------------------------------------- network --


def build_network(seed=11, label_split=(15, 30, 45, 60)):
    schema = RealFeatureSchema.default_social(n_cities=8, n_topics=10)
    return RandomSocialGraphAdvanced(
        labelSplit=list(label_split),
        realFeatureSchema=schema,
        realFeatureSeed=seed,
        connectionPercentageWithMatchedNodes=5,
        explorationProbability=0.5,
        popularityPreferenceIntensity=0.5,
        mutualPreferenceIntensity=[0.9, 0.3, 0.1],
        useGPU=False, createInGPUMem=False,
        keepHistory=False, numberofProcesses=None,
        socialiseOnCreation=True)


def test_end_to_end_network_generation():
    G = build_network()
    assert G.nodeCount == 60
    assert G.edgeCount > 0
    labels = [n.label for n in G.N]
    assert set(labels) == {0, 1, 2, 3}
    # adjacency is symmetric (undirected)
    for (i, j) in list(G.adjMatDict):
        if G.adjMatDict[i, j] is not None:
            assert G.adjMatDict[j, i] == 1
    # every node carries typed values and the numeric encoding
    n0 = G.N[0]
    assert len(n0.featureValues) == G.realFeatureSchema.n_features
    assert len(n0.features) == sum(s.encoded_length()
                                   for s in G.realFeatureSchema.specs)


def test_dynamic_evolution_still_works():
    G = build_network(seed=13)
    edges_before = G.edgeCount
    G.mutateDNA(mutationIntensity=0.2, mutatePreference=True,
                mutatePreferenceProbability=True)
    G.socialise()
    assert G.edgeCount >= edges_before


def test_path_length_terms_are_added_after_first_socialise():
    """Regression: the Eq. 9 path-length scores must contribute additively
    in the default (non-multiplicative) mode -- for both the typed node and
    the original NodeSocial."""
    from scipy.sparse import dok_matrix
    from Node import NodeSocial

    schema = RealFeatureSchema([
        FeatureSpec("age", "numeric", age_sampler, value_range=(0, 100)),
    ])

    def prepared_pair(node_builder):
        g = make_graph_shell()
        dna = DNAadvanced([-1, 0.0], len=1, useGPU=False, createInGPUMem=False)
        dna.preferPopularityIntensity = 0.0
        dna.preferShorterPathIntensity = [0.5, 0.2, 0.1]
        a = node_builder(g, dna, 30)
        b = node_builder(g, dna, 40)
        n = g.nodeCount
        g.adjP2 = dok_matrix((n, n), dtype=int)
        g.adjP3 = dok_matrix((n, n), dtype=int)
        g.adjP4 = dok_matrix((n, n), dtype=int)
        g.adjP2[a.ID, b.ID] = 1  # one 2-path between a and b
        g.Socialised = True
        return a, b

    def typed(g, dna, age):
        return NodeSocialReal(label=0, DNA=dna, Graph=g, schema=schema,
                              featureValues=[age])

    def plain(g, dna, age):
        return NodeSocial(label=0, DNA=dna, Graph=g,
                          additionalFeatures=[age])

    for builder in (typed, plain):
        a, b = prepared_pair(builder)
        with_path = a.getScoreAdvanced(
            b, popularityPreferenceIntensity=0.0,
            mutualPreferenceIntensity=[0.9, 0.3, 0.1])
        without = a.getScoreAdvanced(
            b, popularityPreferenceIntensity=0.0,
            mutualPreferenceIntensity=None)
        # feature weight is 0 and popularity intensity 0, so the only
        # difference must be the 2-path term: mpi * k2 = 0.9 * 0.5
        assert with_path == pytest.approx(without + 0.9 * 0.5), builder.__name__


def test_homophily_emerges_for_similarity_preferring_dna():
    """With all-sDNA forced to prefer-similar on a single categorical
    feature, connected pairs should share the category more often than
    random pairs do."""
    schema = RealFeatureSchema([
        FeatureSpec("city", "categorical",
                    zipf_categorical_sampler(4, s=0.0), n_categories=4),
    ])
    G = RandomSocialGraphAdvanced(
        labelSplit=[40, 80], realFeatureSchema=schema, realFeatureSeed=21,
        connectionPercentageWithMatchedNodes=5, explorationProbability=1.0,
        popularityPreferenceIntensity=0.0,
        mutualPreferenceIntensity=None,
        useGPU=False, createInGPUMem=False, keepHistory=False,
        socialiseOnCreation=False)
    for dna in G.DNA:
        dna.value[0] = -1  # prefer similar
        dna.value[1] = 1.0
        dna.preferPopularityIntensity = 0.0
    G.socialise()
    same = total = 0
    for (i, j) in list(G.adjMatDict):
        if i < j and G.adjMatDict[i, j] is not None:
            total += 1
            if G.N[i].featureValues[0] == G.N[j].featureValues[0]:
                same += 1
    assert total > 0
    # ~25% of random pairs share a uniform 4-way category; homophily
    # should push connected pairs far above that
    assert same / total > 0.5
