# Simulation Core Submodule Architecture Documentation

Core simulation engine submodule that provides low-level simulation functionality and performance metric calculation.

**File List:**
- `__init__.py` - Submodule export interface, exports core simulation functions
- `one_shot_access.py` - Single random access simulation, simulates the access process of a single AC cycle
- `group_paging.py` - Group paging simulation, simulates the complete process of multiple AC cycles, supports multi-threaded parallelization
- `metrics.py` - Performance metric calculation, calculates mean values and confidence intervals for P_S, T_a, P_C

**Please update me if the folder I belong to changes.**

