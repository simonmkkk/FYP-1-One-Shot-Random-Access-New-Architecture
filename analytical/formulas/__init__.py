"""
論文公式模組

導出論文中的所有數學公式。

Input: 系統參數（M, N, k 等）
Output: paper_formula_1 到 paper_formula_10, confidence_interval_95 等
Position: 數學公式的統一入口

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .formulas import (
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
    confidence_interval_95,
    relative_error_percentage,
)

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
    'confidence_interval_95',
    'relative_error_percentage',
]

