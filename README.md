# VirtualSoc
Required packages:

numpy, pandas, scipy, SALib, pathos 

cupy and CUDA for the GPU version. 

For a single network simulation follow the ScriptSingleNetwork.py  
For multiple networks simulation follow the ScriptMultiNetwork.py 

If you have an NVIDIA GPU with CUDA, use the GPU branch, otherwise the CPU branch

Thanks and happy simulation. 


## The paper will be linked soon.


p.s. to calculate the generated network's properties and statistics: 
To calculate network statistics and properties for the generated networks you can use the R script. Use the function pipeNetworkStats("D:/VirtualSocPP1/", threads=7) , and pass the root directory path to the function and number of threads you want it to use. There are dependencies for the r script and they need to be installed to run the script. 
(This R script is separate from this project and relies heavily on other libraries for graph properties algorithm. 
The R script is provided for calculating graph properties but not a part of the VirtualSoc project)
