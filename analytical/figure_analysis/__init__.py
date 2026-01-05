"""
Figure 分析模組

運行各 Figure 的解析計算並保存結果。

Input: config 配置, formulas 公式模組
Output: run_figure*_analysis(), load_figure*_results()
Position: 解析計算的執行層

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .figure1_analysis import run_figure1_analysis, load_figure1_results
from .figure2_analysis import run_figure2_analysis, load_figure2_results
from .figure345_analysis import run_figure345_analysis, load_figure345_results

__all__ = [
    'run_figure1_analysis',
    'run_figure2_analysis', 
    'run_figure345_analysis',
    'load_figure1_results',
    'load_figure2_results',
    'load_figure345_results',
]

