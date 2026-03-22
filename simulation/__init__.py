# ============================================================================
# simulation - One-Shot Random Access Monte Carlo simulation package
# ============================================================================
#
# Package structure:
#   simulation/
#   ├── __init__.py              # Package root (this file)
#   ├── simulation_figure345.py  # Figure 3, 4, 5 simulation entry
#   ├── config/                  # Config files (YAML)
#   └── core/                    # Core modules
#       ├── config.py            # Config dataclass
#       ├── constants.py         # Default constants
#       ├── metrics.py           # Performance metrics
#       ├── one_shot_access.py   # Simulation engine
#       ├── runner.py            # Parallel execution
#       └── utils/
#           └── progress_manager.py  # Rich progress bar
# ============================================================================

# Core module imports
from .core.config import Config
from .core.constants import (
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_I_MAX,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_NUM_WORKERS,
)
from .core.one_shot_access import (
    simulate_one_shot_access_single_ac,
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .core.metrics import SimulationResult, calculate_performance_metrics
from .core.runner import (
    run_single_n_simulation,
    run_n_scan,
    run_experiment,
    save_results_to_csv,
    PROJECT_ROOT,
    SIM_RESULT_ROOT,
)

# Simulation entry point
from .simulation_figure345 import run_figure345

__all__ = [
    # Config
    'Config',
    'DEFAULT_M',
    'DEFAULT_N',
    'DEFAULT_I_MAX',
    'DEFAULT_NUM_SAMPLES',
    'DEFAULT_NUM_WORKERS',
    # Simulation functions
    'simulate_one_shot_access_single_ac',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    # Metrics
    'SimulationResult',
    'calculate_performance_metrics',
    # Runner
    'run_single_n_simulation',
    'run_n_scan',
    'run_experiment',
    'save_results_to_csv',
    'PROJECT_ROOT',
    'SIM_RESULT_ROOT',
    # Entry point
    'run_figure345',
]
