# Input: 依赖figure1、figure2、figure345子模块提供各图表绘图功能
# Output: 导出所有绘图函数供外部使用
# Position: 绘图模块的导出接口，统一对外提供绘图功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

# 繪圖模組
from .figure1 import plot_figure1
from .figure2 import plot_figure2
from .figure345 import plot_figure3, plot_figure4, plot_figure5

__all__ = [
    'plot_figure1',
    'plot_figure2',
    'plot_figure3',
    'plot_figure4',
    'plot_figure5',
]

