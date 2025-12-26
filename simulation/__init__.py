# Input: 依赖core子模块提供单次接入模拟、群组寻呼模拟、性能指标计算功能
# Output: 导出所有模拟相关函数供外部使用
# Position: 模拟模块的导出接口，统一对外提供模拟功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

# 模擬模組
from .core.one_shot_access import simulate_one_shot_access_single_sample
from .core.group_paging import (
    simulate_group_paging_single_sample,
    simulate_group_paging_multi_samples,
)
from .core.metrics import calculate_performance_metrics

__all__ = [
    'simulate_one_shot_access_single_sample',
    'simulate_group_paging_single_sample',
    'simulate_group_paging_multi_samples',
    'calculate_performance_metrics',
]

