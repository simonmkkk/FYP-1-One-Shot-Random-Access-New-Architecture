"""
解析模型模組

提供論文中的數學公式和理論計算功能。

Input: 系統參數（M, N, I_max 等）
Output: 論文公式 1-10, theoretical_calculation(), run_figure*_analysis()
Position: 解析計算的統一入口

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .formulas.formulas import (
    paper_formula_1_pk_probability,
    paper_formula_2_collision_raos_exact,
    paper_formula_3_success_raos_exact,
    paper_formula_4_success_approx,
    paper_formula_5_collision_approx,
    paper_formula_6_success_per_cycle,
    paper_formula_7_next_contending_devices,
    paper_formula_8_access_success_probability,
    paper_formula_9_mean_access_delay,
    paper_formula_10_collision_probability,
)
from .theoretical.theoretical import theoretical_calculation

__all__ = [
    'paper_formula_1_pk_probability',
    'paper_formula_2_collision_raos_exact',
    'paper_formula_3_success_raos_exact',
    'paper_formula_4_success_approx',
    'paper_formula_5_collision_approx',
    'paper_formula_6_success_per_cycle',
    'paper_formula_7_next_contending_devices',
    'paper_formula_8_access_success_probability',
    'paper_formula_9_mean_access_delay',
    'paper_formula_10_collision_probability',
    'theoretical_calculation',
]

