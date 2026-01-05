"""
單次隨機接入模擬模組

模擬一次 One-Shot Random Access（單個 AC）。

Input: M（設備數）, N（RAO 數）
Output: simulate_one_shot_access_single_sample() 返回 (success, collision, idle)
Position: 最底層的單次接入模擬

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import numpy as np


def simulate_one_shot_access_single_sample(M: int, N: int):
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

