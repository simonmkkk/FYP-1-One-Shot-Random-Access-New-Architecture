# ============================================================================
# simulation.core - Core simulation engine
# ============================================================================

from .config import Config
from .constants import (
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_I_MAX,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_NUM_WORKERS,
)
from .one_shot_access import (
    simulate_one_shot_access_single_ac,
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .metrics import SimulationResult, calculate_performance_metrics
from .runner import (
    run_single_n_simulation,
    run_n_scan,
    run_experiment,
    save_results_to_csv,
)
from .paths import (
    PROJECT_ROOT,
    SIMULATION_ROOT,
    create_simulation_run_dir,
    write_metadata,
    relpath,
)

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
    # Paths
    'PROJECT_ROOT',
    'SIMULATION_ROOT',
    'create_simulation_run_dir',
    'write_metadata',
    'relpath',
]
