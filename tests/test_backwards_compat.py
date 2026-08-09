"""The original abstract-feature pipeline must keep working (CPU-only)."""

from Networks import RandomSocialGraphAdvanced


def test_abstract_feature_network_cpu():
    G = RandomSocialGraphAdvanced(
        labelSplit=[10, 20, 30],
        connectionPercentageWithMatchedNodes=5,
        explorationProbability=0.5,
        addTraidtionalFeatures=False,
        additionalFeatureLen=12,
        npDistFunc=['np.random.randint(3, high=500)',
                    'np.random.randint(3, high=500)'],
        popularityPreferenceIntensity=0.5,
        mutualPreferenceIntensity=[0.9, 0.3, 0.1],
        genFeaturesFromSameDistforAllLabel=False,
        keepHistory=False,
        useGPU=False, createInGPUMem=False,
        numberofProcesses=None,
        socialiseOnCreation=True)
    assert G.nodeCount == 30
    assert G.edgeCount > 0
    assert len(G.N[0].features) == 12


def test_traditional_three_features_cpu():
    G = RandomSocialGraphAdvanced(
        labelSplit=[10, 20],
        connectionPercentageWithMatchedNodes=5,
        explorationProbability=0.5,
        addTraidtionalFeatures=True,
        additionalFeatureLen=0,
        npDistFunc=None,
        popularityPreferenceIntensity=0.5,
        mutualPreferenceIntensity=[0.9, 0.3, 0.1],
        genFeaturesFromSameDistforAllLabel=True,
        keepHistory=False,
        useGPU=False, createInGPUMem=False,
        numberofProcesses=None,
        socialiseOnCreation=True)
    assert G.nodeCount == 20
    assert G.edgeCount > 0
    # age, gender, location present (location-assignment bug fixed)
    n = G.N[0]
    assert len(n.features) == 3
    assert hasattr(n, "location")
