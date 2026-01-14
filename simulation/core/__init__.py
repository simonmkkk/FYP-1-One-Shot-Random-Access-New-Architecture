"""
核心模擬模組

提供底層模擬引擎和性能指標計算。

Input: M, N, I_max, num_samples 參數
Output: simulate_one_shot_access_single_ac(), simulate_group_paging_multi_samples()
Position: 模擬系統的核心引擎

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .one_shot_access import (
    simulate_one_shot_access_single_ac,
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .metrics import calculate_performance_metrics

__all__ = [
    'simulate_one_shot_access_single_ac',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    'calculate_performance_metrics',
]

