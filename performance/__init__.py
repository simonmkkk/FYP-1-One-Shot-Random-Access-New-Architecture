"""
性能監測模組

提供簡單的計時功能，測量程序各部分的執行時間。

Input: 計時器名稱和步驟
Output: SimpleTimer 計時器, 樹狀時間報告
Position: 系統性能分析工具

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .simple_timer import (
    SimpleTimer,
    start_timer,
    get_timer,
    clear_timer,
)

__all__ = [
    'SimpleTimer',
    'start_timer',
    'get_timer',
    'clear_timer',
]

