# Input: 依赖numpy进行统计计算（均值、标准差、置信区间）
# Output: 提供calculate_performance_metrics和confidence_interval_95函数，计算P_S、T_a、P_C的均值和置信区间
# Position: 模拟模块的指标计算模块，将模拟结果转换为性能指标
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

"""
性能指標計算模組
"""

import numpy as np


def confidence_interval_95(data):
    """計算95%置信區間（半寬）"""
    return 1.96 * np.std(data) / np.sqrt(len(data))


def calculate_performance_metrics(results_array):
    """
    計算平均性能指標
    
    Args:
        results_array: 模擬結果數組 [num_samples, 3]
    
    Returns:
        tuple: ((mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc))
    """
    mean_ps = np.mean(results_array[:, 0])
    mean_pc = np.mean(results_array[:, 2])
    
    valid_ta_samples = results_array[results_array[:, 1] >= 0, 1]
    if len(valid_ta_samples) > 0:
        mean_ta = np.mean(valid_ta_samples)
        ci_ta = confidence_interval_95(valid_ta_samples)
    else:
        mean_ta = 0
        ci_ta = 0
    
    ci_ps = confidence_interval_95(results_array[:, 0])
    ci_pc = confidence_interval_95(results_array[:, 2])
    
    return (mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc)

