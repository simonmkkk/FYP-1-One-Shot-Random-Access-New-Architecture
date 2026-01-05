"""
理論計算核心實現

使用論文公式迭代計算 P_S、T_a、P_C 等性能指標。

Input: M（設備數）, N（RAO 數）, I_max（最大 AC 數）
Output: theoretical_calculation() 返回完整性能指標
Position: 解析計算的數學引擎

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import numpy as np
from ..formulas.formulas import (
    paper_formula_5_collision_approx,
    paper_formula_6_success_per_cycle,
    paper_formula_7_next_contending_devices, 
    paper_formula_8_access_success_probability,
    paper_formula_9_mean_access_delay,
    paper_formula_10_collision_probability
    
)


def theoretical_calculation(M, N, I_max):
    """
    使用论文中的理论方法计算性能指标
    
    Args:
        M: 設備總數
        N: 每個AC的RAO數
        I_max: 最大AC數
    
    Returns:
        tuple: (P_S, T_a, P_C, N_s_list, K_list)
    """
    K = [M]
    N_s = []
    N_c = []
    
    for i in range(1, I_max + 1):
        if len(K) <= i-1 or K[i-1] <= 0:
            N_s.append(0)
            N_c.append(0)
            K.append(0)
            continue
        
        current_K = K[i-1]
        N_s_i = paper_formula_6_success_per_cycle(current_K, N)
        N_s.append(N_s_i)
        
        N_c_i = paper_formula_5_collision_approx(current_K, N)
        N_c.append(N_c_i)
        
        K_i_plus_1 = paper_formula_7_next_contending_devices(current_K, N)
        K.append(K_i_plus_1)
    
    P_S = paper_formula_8_access_success_probability(N_s, M)
    T_a = paper_formula_9_mean_access_delay(N_s)
    P_C = paper_formula_10_collision_probability(N_c, I_max, N)
    
    return P_S, T_a, P_C, N_s, K

