"""
============================================================================
simulation 套件根目錄
============================================================================

提供 One-Shot Random Access 蒙特卡洛模擬功能。

用法示例：
    from simulation import Config                 # 導入配置類
    from simulation import run_experiment         # 導入實驗入口
    from simulation import run_figure345          # 導入 Figure 3,4,5 模擬

套件結構：
    simulation/
    ├── __init__.py              # 此文件，套件入口
    ├── simulation_figure345.py  # Figure 3,4,5 模擬入口
    ├── config/                  # 配置文件目錄
    │   ├── default_config.yaml
    │   └── simulation_figure345.yaml
    ├── core/                    # 核心模組目錄
    │   ├── __init__.py          # 核心模組入口
    │   ├── config.py            # 配置類
    │   ├── constants.py         # 常數定義
    │   ├── metrics.py           # 統計指標
    │   ├── one_shot_access.py   # 模擬引擎
    │   └── runner.py            # 並行執行器
    └── figure_simulation/       # Figure 模擬目錄（舊版兼容）

架構重構日期: 2026-01-24
============================================================================
"""

# ============================================================================
# 核心模組導入
# ============================================================================
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

# ============================================================================
# 模擬入口函數導入
# ============================================================================
from .simulation_figure345 import run_figure345

# ============================================================================
# 模組導出列表
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
    # 模擬入口
    'run_figure345',
]
