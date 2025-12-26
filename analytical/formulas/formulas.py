# Input: 依赖numpy、math模块进行数学计算
# Output: 提供论文10个公式的实现函数（精确公式、近似公式、迭代公式、性能指标公式）
# Position: 解析模型的基础模块，提供所有数学公式的底层实现
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

"""
論文數學公式模組

基於論文: "Modeling and Estimation of Single Random Access for 
          Finite-User Multi-Channel Slotted ALOHA Systems"

公式架構：
├── 精確公式 (1-3) - 單次隨機接入分析
├── 近似公式 (4-5) - 快速計算
├── 迭代公式 (6-7) - 多個AC循環
└── 性能指標公式 (8-10)
"""

import numpy as np
from math import factorial, comb
from functools import lru_cache


# ============================================================================
# 輔助工具函數
# ============================================================================

def generate_partitions(n: int, k: int, min_val: int = 2):
    """
    生成所有满足条件的整數分割
    
    功能：生成滿足 i1+i2+...+ik = n, 每個ij >= min_val 的所有分割
    """
    if k == 0:
        if n == 0:
            yield []
        return
    if k == 1:
        if n >= min_val:
            yield [n]
        return
    
    for first in range(min_val, n - min_val * (k - 1) + 1):
        for rest in generate_partitions(n - first, k - 1, min_val):
            yield [first] + rest

@lru_cache(maxsize=10000)
def compute_configuration_ways(M: int, N1: int, k: int, total_in_collision: int, remaining_users: int) -> int:
    """計算給定碰撞配置的方式數"""
    ways_this_config = 0
    
    if k == 0:
        if total_in_collision == 0 and remaining_users <= N1:
            ways_non_collision = comb(N1, remaining_users) * factorial(remaining_users)
            ways_this_config = ways_non_collision
    else:
        partitions = generate_partitions(total_in_collision, k, 2)
        for partition in partitions:
            ways_collision = 1
            remaining = M
            for count in partition:
                ways_collision *= comb(remaining, count)
                remaining -= count
            
            ways_non_collision = comb(N1 - k, remaining_users) * factorial(remaining_users)
            ways_specific_assignment = ways_collision * ways_non_collision
            ways_choose_collision_raos = comb(N1, k)
            ways_this_config += ways_specific_assignment * ways_choose_collision_raos
    
    return ways_this_config


# ============================================================================
# 精確公式 (1-3) - 單次隨機接入分析
# ============================================================================

def paper_formula_1_pk_probability(M: int, N1: int, k: int) -> float:
    """
    【公式1】pk(M, N1) - k個碰撞RAO的概率
    
    論文對應：Section II-B, Equation (1)
    """
    return paper_formula_1_pk_probability_impl(M, N1, k)


@lru_cache(maxsize=20000)
def paper_formula_1_pk_probability_impl(M: int, N1: int, k: int) -> float:
    """公式(1)的實際計算函數（帶LRU快取）"""
    if k < 0 or k > min(N1, M // 2):
        return 0.0
    
    total_ways = N1 ** M
    valid_ways = 0
    
    for total_in_collision in range(2 * k, M + 1):
        remaining_users = M - total_in_collision
        if remaining_users > N1 - k:
            continue
        valid_ways += compute_configuration_ways(M, N1, k, total_in_collision, remaining_users)
    
    pk = valid_ways / total_ways if total_ways > 0 else 0.0
    return pk


def paper_formula_2_collision_raos_exact(M: int, N1: int) -> float:
    """
    【公式2】NC,1 - 期望碰撞RAO數（精確）
    
    論文對應：Section II-B, Equation (2)
    """
    if M <= 1 or N1 == 0:
        return 0.0
    
    NC_1 = 0.0
    max_k = min(N1, M // 2)
    
    for k in range(1, max_k + 1):
        pk_val = paper_formula_1_pk_probability(M, N1, k)
        NC_1 += k * pk_val
    
    return NC_1


def paper_formula_3_success_raos_exact(M: int, N1: int) -> float:
    """
    【公式3】NS,1 - 期望成功RAO數（精確）
    
    論文對應：Section II-B, Equation (3)
    """
    if M == 0 or N1 == 0:
        return 0.0
    
    NS_1 = 0.0
    max_k = min(N1, M // 2)
    
    for k in range(0, max_k + 1):
        pk_val = paper_formula_1_pk_probability(M, N1, k)
        
        if pk_val == 0:
            continue
        
        expected_success_given_k = 0.0
        
        for total_in_collision in range(2 * k if k > 0 else 0, M + 1):
            remaining_users = M - total_in_collision
            
            if remaining_users > N1 - k:
                continue
            
            ways_this_config = compute_configuration_ways(M, N1, k, total_in_collision, remaining_users)
            total_ways = N1 ** M
            prob_this_config = ways_this_config / total_ways if total_ways > 0 else 0
            
            if prob_this_config > 0:
                expected_success_given_k += remaining_users * (prob_this_config / pk_val)
        
        NS_1 += expected_success_given_k * pk_val
    
    return NS_1


# ============================================================================
# 近似公式 (4-5) - 快速計算版本
# ============================================================================

def paper_formula_4_success_approx(M, N1):
    """
    【公式4】NS,1 ≈ M·e^(-M/N1) - 成功RAO近似公式
    
    論文對應：Section II-C, Equation (4)
    """
    return M * np.exp(-M / N1)


def paper_formula_5_collision_approx(M, N1):
    """
    【公式5】NC,1 ≈ N1·(1 - e^(-M/N1)·(1 + M/N1)) - 碰撞RAO近似公式
    
    論文對應：Section II-C, Equation (5)
    """
    exp_term = np.exp(-M / N1)
    return N1 * (1 - exp_term * (1 + M/N1))


# ============================================================================
# 迭代公式 (6-7) - 多個AC循環
# ============================================================================

def paper_formula_6_success_per_cycle(K_i, N_i):
    """
    【公式6】NS,i = Ki·e^(-Ki/Ni) - 第i個AC的成功設備數
    
    論文對應：Section III-A, Equation (6)
    """
    return K_i * np.exp(-K_i / N_i)


def paper_formula_7_next_contending_devices(K_i, N_i):
    """
    【公式7】Ki+1 = Ki·(1 - e^(-Ki/Ni)) - 下一個AC的競爭設備數
    
    論文對應：Section III-A, Equation (7)
    """
    return K_i * (1 - np.exp(-K_i / N_i))


# ============================================================================
# 性能指標公式 (8-10)
# ============================================================================

def paper_formula_8_access_success_probability(N_s_list, M):
    """
    【公式8】PS = Σ NS,i / M - 接入成功概率
    
    論文對應：Section III-A, Equation (8)
    """
    total_success = sum(N_s_list)
    return total_success / M if M > 0 else 0


def paper_formula_9_mean_access_delay(N_s_list):
    """
    【公式9】Ta = Σ(i·NS,i) / Σ NS,i - 平均接入延遲
    
    論文對應：Section III-A, Equation (9)
    """
    total_success = sum(N_s_list)
    if total_success <= 0:
        return 0
    
    weighted_sum = sum((i + 1) * N_s for i, N_s in enumerate(N_s_list))
    return weighted_sum / total_success


def paper_formula_10_collision_probability(N_c_list, I_max, N):
    """
    【公式10】PC = Σ NC,i / (I_max × N) - 碰撞概率
    
    論文對應：Section III-A, Equation (10)
    """
    total_collision = sum(N_c_list)
    total_rao = I_max * N
    return total_collision / total_rao if total_rao > 0 else 0


# ============================================================================
# 工具函數
# ============================================================================

def confidence_interval_95(data):
    """計算95%置信區間（半寬）"""
    return 1.96 * np.std(data) / np.sqrt(len(data))


def relative_error_percentage(theoretical, actual):
    """計算相對誤差百分比"""
    if theoretical != 0:
        return abs(actual - theoretical) / abs(theoretical) * 100
    else:
        return abs(actual - theoretical) * 100

