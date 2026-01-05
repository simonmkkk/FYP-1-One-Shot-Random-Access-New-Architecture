"""
繪圖模組

提供論文各 Figure 的可視化功能。

Input: analytical/simulation 計算結果
Output: plot_figure1/2/3/4/5() 繪圖函數
Position: 數據可視化的統一入口

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

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

