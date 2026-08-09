"""Example: simulate a social network with realistic, typed features.

Instead of abstract numbers, every node gets age, gender, city, a
geographic position, education level and an interest set, each compared
with a type-aware dissimilarity inside the sDNA score (see
RealFeatures.py). Everything else -- sDNA labels, preferential
attachment, path-length preference, mutation/dynamics -- works exactly
as in the paper (arXiv:1905.09087).
"""

import numpy as np

from Networks import RandomSocialGraphAdvanced
from RealFeatures import RealFeatureSchema

if __name__ == '__main__':
    schema = RealFeatureSchema.default_social(n_cities=20, n_topics=15)

    G = RandomSocialGraphAdvanced(
        labelSplit=[50, 100, 150, 200],     # four sDNA groups of 50 nodes
        realFeatureSchema=schema,           # <- typed features switch
        realFeatureSeed=42,
        connectionPercentageWithMatchedNodes=5,
        explorationProbability=0.3,
        popularityPreferenceIntensity=0.5,
        mutualPreferenceIntensity=[0.9, 0.3, 0.1],
        useGPU=False, createInGPUMem=False,
        keepHistory=False,
        socialiseOnCreation=True,
    )

    # two evolution steps with preference drift, as in the paper
    G.mutateDNA(mutationIntensity=0.01, mutatePreference=True,
                mutatePreferenceProbability=True)
    G.socialise()

    print(f"\nnodes: {G.nodeCount}, edges: {int(G.edgeCount)}")

    n = G.N[0]
    named = dict(zip((s.name for s in schema.specs), n.featureValues))
    print(f"example node (label {n.label}): {named}")
    print(f"encoded feature vector length (for GCN training): "
          f"{len(n.features)} -> {schema.encoded_feature_names()[:6]} ...")

    # homophily snapshot: how often connected pairs share city / gender
    same_city = same_gender = total = 0
    city_ix = [s.name for s in schema.specs].index("city")
    gender_ix = [s.name for s in schema.specs].index("gender")
    for (i, j) in list(G.adjMatDict):
        if i < j and G.adjMatDict[i, j] is not None:
            total += 1
            same_city += G.N[i].featureValues[city_ix] == G.N[j].featureValues[city_ix]
            same_gender += G.N[i].featureValues[gender_ix] == G.N[j].featureValues[gender_ix]
    if total:
        print(f"connected pairs sharing city: {same_city / total:.2%}, "
              f"sharing gender: {same_gender / total:.2%} ({total} edges)")

    # GCN-ready exports
    X = np.array([node.features for node in G.N])
    y = np.array([node.label for node in G.N])
    print(f"feature matrix X: {X.shape}, labels y: {y.shape}, "
          f"classes: {sorted(set(y.tolist()))}")
