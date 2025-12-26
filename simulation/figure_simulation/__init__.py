# Input: 依赖figure345_simulation子模块提供图表模拟功能
# Output: 导出run_figure345_simulation和load_figure345_simulation_results函数供外部使用
# Position: 图表模拟子模块的导出接口，统一对外提供图表模拟功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

# Figure 模擬模組
from .figure345_simulation import run_figure345_simulation, load_figure345_simulation_results

__all__ = [
    'run_figure345_simulation',
    'load_figure345_simulation_results',
]

