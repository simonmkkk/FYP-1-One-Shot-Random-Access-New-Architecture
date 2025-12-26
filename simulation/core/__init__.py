# Input: 依赖one_shot_access、group_paging、metrics子模块提供核心模拟功能
# Output: 导出所有核心模拟函数供外部使用
# Position: 核心模拟引擎子模块的导出接口，统一对外提供底层模拟功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

# 核心模擬模組
from .one_shot_access import simulate_one_shot_access_single_sample
from .group_paging import (
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .metrics import calculate_performance_metrics

__all__ = [
    'simulate_one_shot_access_single_sample',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    'calculate_performance_metrics',
]

