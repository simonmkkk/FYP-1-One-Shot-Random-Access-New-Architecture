"""
Figure 模擬模組

運行各 Figure 的蒙特卡洛模擬。

Input: config 配置, group_paging 模擬引擎
Output: run_figure345_simulation(), load_figure345_simulation_results()
Position: 模擬任務的執行層

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .figure345_simulation import run_figure345_simulation, load_figure345_simulation_results

__all__ = [
    'run_figure345_simulation',
    'load_figure345_simulation_results',
]

