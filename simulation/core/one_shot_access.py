"""
單次隨機接入模擬模組

模擬一次 One-Shot Random Access（單個 AC）。

Input: M（設備數）, N（RAO 數）
Output: simulate_one_shot_access_single_ac() 返回 (success, collision, idle)
Position: 最底層的單次接入模擬

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import numpy as np


def simulate_one_shot_access_single_ac(M: int, N: int):
    """
    模擬一次 One-Shot Random Access（單個 AC）
    
    Args:
        M: 嘗試接入的設備數量
        N: 可用的 RAO 數量
    
    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
    """
    choices = np.random.randint(0, N, M)
    rao_usage = np.bincount(choices, minlength=N)
    
    success_raos = np.sum(rao_usage == 1)
    collision_raos = np.sum(rao_usage >= 2)
    idle_raos = np.sum(rao_usage == 0)
    
    return success_raos, collision_raos, idle_raos


def simulate_one_shot_access_single_ac_rng(M: int, N: int, rng: np.random.Generator):
    """
    模擬一次 One-Shot Random Access（單個 AC）- RNG 優化版本
    
    使用 numpy 的 Generator API 實現更快速且線程安全的隨機數生成。
    相比 legacy np.random，速度提升約 2-3 倍。
    
    Args:
        M: 嘗試接入的設備數量
        N: 可用的 RAO 數量
        rng: numpy Generator 實例（由 np.random.default_rng() 創建）
    
    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
    """
    # 使用 rng.integers 替代 np.random.randint（更快）
    choices = rng.integers(0, N, size=M)
    rao_usage = np.bincount(choices, minlength=N)
    
    success_raos = np.sum(rao_usage == 1)
    collision_raos = np.sum(rao_usage >= 2)
    idle_raos = np.sum(rao_usage == 0)
    
    return success_raos, collision_raos, idle_raos

