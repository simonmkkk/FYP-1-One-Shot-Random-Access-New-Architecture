"""
============================================================================
核心模擬模組
============================================================================

提供底層模擬引擎和性能指標計算。

Input: M, N, I_max, num_samples 參數
Output: Config, SimulationResult, 模擬函數, runner 函數
Position: 模擬系統的核心引擎

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 配置類導入
# ============================================================================
from .config import Config
from .constants import (
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_I_MAX,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_NUM_WORKERS,
)

# ============================================================================
# 模擬函數導入
# ============================================================================
from .one_shot_access import (
    simulate_one_shot_access_single_ac,
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)

# ============================================================================
# 統計類導入
# ============================================================================
from .metrics import SimulationResult, calculate_performance_metrics

# ============================================================================
# Runner 函數導入
# ============================================================================
from .runner import (
    run_single_n_simulation,
    run_n_scan,
    run_experiment,
    save_results_to_csv,
    PROJECT_ROOT,
    SIM_RESULT_ROOT,
)

# ============================================================================
# 模組導出
# ============================================================================
__all__ = [
    # 配置類
    'Config',
    'DEFAULT_M',
    'DEFAULT_N',
    'DEFAULT_I_MAX',
    'DEFAULT_NUM_SAMPLES',
    'DEFAULT_NUM_WORKERS',
    # 模擬函數
    'simulate_one_shot_access_single_ac',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    # 統計類
    'SimulationResult',
    'calculate_performance_metrics',
    # Runner 函數
    'run_single_n_simulation',
    'run_n_scan',
    'run_experiment',
    'save_results_to_csv',
    'PROJECT_ROOT',
    'SIM_RESULT_ROOT',
]
