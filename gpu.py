"""Optional CuPy import.

VirtualSoc uses CuPy for GPU-accelerated score calculation when available.
Importing this module never fails: on machines without CuPy (or with a
broken CUDA setup) ``cp`` is None and ``GPU_AVAILABLE`` is False, and the
library runs entirely on the CPU.
"""

try:
    import cupy as cp
    GPU_AVAILABLE = bool(cp.cuda.is_available())
except Exception:  # ImportError, or CUDA runtime failures on import
    cp = None
    GPU_AVAILABLE = False
