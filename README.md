

# VirtualSoc
# Simulate Dynamic Social Networks with ground truth labels and features.

Required packages:

numpy, pandas, SciPy, SALib, pathos, PyPrind 

cupy and CUDA for the GPU version. 

For a single network simulation follow the ScriptSingleNetwork.py  
For multiple networks simulation follow the ScriptMultiNetwork.py 

CuPy/CUDA is now optional: without CuPy installed everything runs on the
CPU automatically (install `cupy-cuda12x` to enable the GPU score path).

Thanks and happy simulation. 

## New: realistic, typed features (age, gender, city, ...)

Besides abstract numeric features, networks can now be simulated with
**typed real-world features** compared by type-aware dissimilarities
inside the sDNA score — see `RealFeatures.py`:

| type | example | dissimilarity |
|---|---|---|
| numeric | age, education | abs. difference / range |
| binary / categorical | gender, city | match / mismatch |
| geo | (x, y) position | euclidean distance |
| multihot | interest sets | 1 − Jaccard overlap |

```python
from RealFeatures import RealFeatureSchema
from Networks import RandomSocialGraphAdvanced

schema = RealFeatureSchema.default_social()   # age, gender, city, geo,
                                              # education, interests
G = RandomSocialGraphAdvanced(labelSplit=[50, 100, 150, 200],
                              realFeatureSchema=schema,
                              useGPU=False, createInGPUMem=False)
```

sDNA semantics are unchanged (per-feature prefer-similar/dissimilar and
weight, mutation, labels), and every node still exposes a flat numeric
encoding (`node.features`: normalised numerics, one-hot categoricals,
0/1 interest vectors) so exports and GCN training work as before.
Custom features are one `FeatureSpec(name, kind, sampler, ...)` each.
Full example: `ScriptRealFeaturesNetwork.py`; tests: `tests/`.

## The paper (preprint) : https://arxiv.org/abs/1905.09087 (Simulation and Augmentation of Social Networks for Building Deep Learning Models)


p.s. to calculate the generated network's properties and statistics: 
To calculate network statistics and properties for the generated networks you can use the R script. Use the function pipeNetworkStats("D:/VirtualSocPP1/", threads=7) , and pass the root directory path to the function and number of threads you want it to use. There are dependencies for the r script and they need to be installed to run the script. 
(This R script is separate from this project and relies heavily on other libraries for graph properties algorithm. 
The R script is provided for calculating graph properties but not a part of the VirtualSoc project)

## Few generated sample datasets are uploaded to the repo. data_sample.zip 
## Many more generated datasets from VirtualSoc https://www.kaggle.com/akandaashraf/virtualsoc1

