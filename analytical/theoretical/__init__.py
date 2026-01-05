"""
理論計算模組

使用論文公式計算系統性能指標。

Input: M, N, I_max 參數
Output: theoretical_calculation() 返回 (P_S, T_a, P_C, N_s_list, K_list)
Position: 解析計算的核心引擎

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .theoretical import theoretical_calculation

__all__ = [
    'theoretical_calculation',
]

