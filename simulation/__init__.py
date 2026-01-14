"""
模擬模組

提供蒙特卡洛模擬功能。

Input: 系統參數（M, N, I_max, num_samples）
Output: simulate_one_shot_access_single_ac(), simulate_group_paging_multi_samples()
Position: 蒙特卡洛模擬的統一入口

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .core.one_shot_access import simulate_one_shot_access_single_ac
from .core.group_paging import (
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .core.metrics import calculate_performance_metrics

__all__ = [
    'simulate_one_shot_access_single_ac',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    'calculate_performance_metrics',
]

