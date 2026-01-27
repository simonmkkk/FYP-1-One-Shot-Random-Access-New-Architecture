"""
============================================================================
metrics - 性能指標計算模組
============================================================================

計算模擬結果的統計指標和置信區間。

提供以下功能：
1. SimulationResult 數據類 - 儲存結構化的模擬結果
2. confidence_interval_95() - 計算 95% 置信區間
3. calculate_performance_metrics() - 計算均值和置信區間

Input: 模擬結果數組 [num_samples, 3]
Output: SimulationResult, calculate_performance_metrics()
Position: 模擬結果的統計處理層

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 標準庫導入
# ============================================================================
from __future__ import annotations  # 啟用延遲類型註解評估

from dataclasses import dataclass  # dataclass 裝飾器，簡化類別定義
from typing import Tuple  # 類型提示工具

import numpy as np  # NumPy 數值計算庫


# ============================================================================
# 模擬結果類
# ============================================================================

@dataclass
class SimulationResult:
    """
    模擬結果類 - 儲存單次 N 值模擬的統計指標
    
    此類為一個 dataclass，用於結構化儲存模擬結果。
    每個實例代表一個 N 值的完整模擬結果。
    
    Attributes:
        N: RAO 數量（Preamble pool size）
        M: 初始設備數量（嘗試接入的 UE 數）
        I_max: 最大 Access Cycle 數
        num_samples: 模擬樣本數
        mean_ps: 平均接入成功率 (P_S)，範圍 [0, 1]
        mean_ta: 平均接入延遲 (T_a)，單位為 AC 數
        mean_pc: 平均碰撞概率 (P_C)，範圍 [0, 1]
        ci_ps: P_S 的 95% 置信區間（半寬）
        ci_ta: T_a 的 95% 置信區間（半寬）
        ci_pc: P_C 的 95% 置信區間（半寬）
    """
    N: int                     # RAO 數量
    M: int                     # 初始設備數量
    I_max: int                 # 最大 Access Cycle 數
    num_samples: int           # 模擬樣本數
    mean_ps: float = 0.0       # 平均接入成功率
    mean_ta: float = 0.0       # 平均接入延遲
    mean_pc: float = 0.0       # 平均碰撞概率
    ci_ps: float = 0.0         # P_S 置信區間
    ci_ta: float = 0.0         # T_a 置信區間
    ci_pc: float = 0.0         # P_C 置信區間


# ============================================================================
# 統計函數
# ============================================================================

def confidence_interval_95(data: np.ndarray) -> float:
    """
    計算 95% 置信區間（半寬）
    
    使用 z = 1.96（對應 95% 置信水平）計算置信區間半寬。
    公式：CI = z * (σ / √n)
    
    Args:
        data: 樣本數據陣列
        
    Returns:
        float: 95% 置信區間半寬
    """
    # 參數說明（來源 + 是什麼）
    # - data: np.ndarray（樣本數據陣列）
    #   來源：由 calculate_performance_metrics 提取的模擬結果列
    
    if len(data) == 0:  # 空數據檢查
        return 0.0
    # z = 1.96 對應 95% 置信水平
    # σ = np.std(data) 樣本標準差
    # n = len(data) 樣本大小
    return 1.96 * np.std(data) / np.sqrt(len(data))  # CI = z * (σ / √n)


def calculate_performance_metrics(results_array: np.ndarray) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """
    計算平均性能指標
    
    從模擬結果數組中計算三個性能指標的均值和置信區間：
    1. P_S (Access Success Probability) - 接入成功率
    2. T_a (Mean Access Delay) - 平均接入延遲
    3. P_C (Collision Probability) - 碰撞概率
    
    注意：T_a 只統計有效樣本（延遲 >= 0），因為 -1 表示無有效延遲
    
    Args:
        results_array: 模擬結果數組，Shape [num_samples, 3]
            - 列 0: Access Success Probability (P_S)
            - 列 1: Mean Access Delay (T_a)
            - 列 2: Collision Probability (P_C)
    
    Returns:
        tuple: ((mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc))
            - 第一個元組：三個指標的均值
            - 第二個元組：三個指標的 95% 置信區間
    """
    # 參數說明（來源 + 是什麼）
    # - results_array: np.ndarray，Shape [num_samples, 3]
    #   來源：simulate_group_paging_multi_samples() 的返回值
    #   結構：每行是一次完整 Group Paging 模擬的結果
    
    # ------------------------------------------------------------------------
    # 計算 P_S（接入成功率）均值
    # ------------------------------------------------------------------------
    mean_ps = np.mean(results_array[:, 0])  # 列 0 的均值
    
    # ------------------------------------------------------------------------
    # 計算 P_C（碰撞概率）均值
    # ------------------------------------------------------------------------
    mean_pc = np.mean(results_array[:, 2])  # 列 2 的均值
    
    # ------------------------------------------------------------------------
    # 計算 T_a（平均接入延遲）均值
    # ------------------------------------------------------------------------
    # 過濾有效樣本：延遲 >= 0（-1 表示無有效延遲，即無設備成功接入）
    valid_ta_samples = results_array[results_array[:, 1] >= 0, 1]  # 過濾有效延遲
    if len(valid_ta_samples) > 0:  # 有有效樣本
        mean_ta = np.mean(valid_ta_samples)  # 有效樣本的均值
        ci_ta = confidence_interval_95(valid_ta_samples)  # 有效樣本的置信區間
    else:  # 無有效樣本
        mean_ta = 0  # 延遲設為 0
        ci_ta = 0  # 置信區間設為 0
    
    # ------------------------------------------------------------------------
    # 計算置信區間
    # ------------------------------------------------------------------------
    ci_ps = confidence_interval_95(results_array[:, 0])  # P_S 的置信區間
    ci_pc = confidence_interval_95(results_array[:, 2])  # P_C 的置信區間
    
    return (mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc)  # 返回均值和置信區間


# ============================================================================
# 模組導出
# ============================================================================

__all__ = [
    "SimulationResult",              # 模擬結果數據類
    "confidence_interval_95",        # 95% 置信區間計算
    "calculate_performance_metrics", # 性能指標計算
]
