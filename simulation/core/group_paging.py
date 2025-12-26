# Input: 依赖one_shot_access模块模拟单次接入，依赖ThreadPoolExecutor实现多线程并行，依赖tqdm显示进度
# Output: 提供simulate_group_paging_single_sample和simulate_group_paging_multi_samples函数，模拟多AC周期的群组寻呼过程
# Position: 模拟模块的核心引擎，提供多周期模拟和多样本并行计算功能
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

"""
群組尋呼模擬模組

模擬完整的群組尋呼過程（多個 AC）

Python 3.14+ Free-threaded 優化版本
使用 ThreadPoolExecutor 實現真正的多線程並行

優化策略：
1. 批量預生成隨機數 (減少 np.random 調用次數)
2. Thread-local RNG (避免重複創建 Generator)
3. 純 Python dict 計數 (對稀疏情況更高效)
4. 預分配 numpy array (減少記憶體碎片和峰值用量)
"""

import os
import time
import threading
import numpy as np
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from tqdm import tqdm

from .one_shot_access import simulate_one_shot_access_single_sample


# Thread-local storage for RNG (每個線程一個 Generator，避免重複創建)
_thread_local = threading.local()

def _get_thread_rng():
    """獲取當前線程的隨機數生成器"""
    if not hasattr(_thread_local, 'rng'):
        _thread_local.rng = np.random.default_rng()
    return _thread_local.rng


def clear_thread_local_rng():
    """清理 thread-local RNG，釋放記憶體"""
    global _thread_local
    _thread_local = threading.local()


def simulate_group_paging_single_sample(M: int, N: int, I_max: int):
    """
    模擬一次完整的群組尋呼過程
    
    優化策略：
    1. 使用 thread-local RNG，避免每次創建新的 Generator
    2. 批量預生成所有 AC 所需的隨機數
    3. 使用純 Python dict 計數（對 M < N 的稀疏情況更高效）
    
    Args:
        M: 初始設備數
        N: 每個 AC 的 RAO 數
        I_max: 最大 AC 數
    
    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
    """
    # 使用 thread-local RNG 批量生成隨機數
    rng = _get_thread_rng()
    all_random_choices = rng.integers(0, N, (I_max, M))
    
    remaining_devices = M
    success_count = 0
    success_delay_sum = 0
    total_collision_count = 0
    
    for ac_index in range(1, I_max + 1):
        if remaining_devices == 0:
            continue
        
        # 使用預生成的隨機數，只取前 remaining_devices 個
        choices = all_random_choices[ac_index - 1, :remaining_devices]
        
        # 純 Python dict 計數 (比 np.bincount 在稀疏情況下更快)
        counts = {}
        for c in choices:
            counts[c] = counts.get(c, 0) + 1
        
        # 計算成功和碰撞
        success_raos = sum(1 for v in counts.values() if v == 1)
        collision_raos = sum(1 for v in counts.values() if v >= 2)
        
        success_count += success_raos
        success_delay_sum += success_raos * ac_index
        total_collision_count += collision_raos
        remaining_devices = remaining_devices - success_raos
    
    access_success_prob = success_count / M if M > 0 else 0.0
    
    if success_count > 0:
        mean_access_delay = success_delay_sum / success_count
    else:
        mean_access_delay = -1.0
    
    total_rao_count = I_max * N
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0
    
    return access_success_prob, mean_access_delay, collision_prob


def _single_sample_worker(args):
    """
    單樣本 worker：執行一個樣本模擬並直接寫入共享 array
    """
    M, N, I_max, idx, results_array = args
    result = simulate_group_paging_single_sample(M, N, I_max)
    results_array[idx, 0] = result[0]
    results_array[idx, 1] = result[1]
    results_array[idx, 2] = result[2]
    return idx


def _micro_batch_worker(args):
    """
    微批次 worker：執行多個樣本模擬並直接寫入共享 array
    用於減少任務調度開銷，提高 CPU 利用率
    """
    M, N, I_max, start_idx, count, results_array = args
    for i in range(count):
        result = simulate_group_paging_single_sample(M, N, I_max)
        idx = start_idx + i
        results_array[idx, 0] = result[0]
        results_array[idx, 1] = result[1]
        results_array[idx, 2] = result[2]
    return count


def simulate_group_paging_multi_samples(M: int, N: int, I_max: int, num_samples: int, 
                                        num_workers: int):
    """
    並行執行完整群組尋呼過程的多樣本模擬（自適應微批次模式）
    
    自適應策略：
    - 根據 M/N 比例調整微批次大小
    - N 越大（M/N 越小），單樣本計算越快，需要更大的微批次來攤平調度開銷
    - 保持約 200-500 個任務，平衡進度更新頻率和 CPU 利用率
    
    Args:
        M: 初始設備總數
        N: 每個 AC 的 RAO 數量
        I_max: 最大接入周期數
        num_samples: 模擬樣本數
        num_workers: 並行工作線程數 (-1 表示使用所有 CPU 核心)
    
    Returns:
        np.ndarray: Shape [num_samples, 3] 的結果矩陣
    """
    if num_workers == -1:
        num_workers = os.cpu_count() or 1
    
    # 自適應微批次大小計算
    # 當 M/N 小時（N 大），單樣本計算快，需要更大的微批次
    # 當 M/N 大時（N 小），單樣本計算慢，可以用較小的微批次
    load_ratio = M / N
    
    # M=100 的情況：
    # N=5  → M/N=20  → 高負載，計算慢，微批次小
    # N=20 → M/N=5   → 中負載
    # N=40 → M/N=2.5 → 低負載，計算快，微批次大
    # N=45 → M/N=2.2 → 低負載，計算快，微批次大
    
    if load_ratio >= 10:
        # 極高負載 (N 很小，如 N=5,10)：單樣本計算很慢
        micro_batch_size = 20
    elif load_ratio >= 5:
        # 高負載 (N 較小，如 N=20)：單樣本計算慢
        micro_batch_size = 50
    elif load_ratio >= 3:
        # 中負載 (N 中等，如 N=30-35)
        micro_batch_size = 150
    else:
        # 低負載 (N 大，如 N=40-45)：單樣本計算快，用大微批次
        micro_batch_size = 500
    
    # 確保任務數量合理（約 200-1000 個任務）
    target_tasks = 500
    calculated_batch = num_samples // target_tasks
    micro_batch_size = max(micro_batch_size, calculated_batch)
    micro_batch_size = min(micro_batch_size, num_samples // (num_workers * 4))  # 至少每個 worker 能分到 4 個任務
    micro_batch_size = max(1, micro_batch_size)  # 最小為 1
    
    num_tasks = (num_samples + micro_batch_size - 1) // micro_batch_size
    
    print("=" * 70)
    print("【Group Paging】完整群組尋呼多樣本並行模擬（自適應微批次）")
    print("=" * 70)
    print(f"  參數配置:")
    print(f"    - 設備數 M = {M}")
    print(f"    - RAO 數 N = {N}")
    print(f"    - 最大 AC 數 I_max = {I_max}")
    print(f"    - 模擬樣本數 = {num_samples:,}")
    print(f"    - 並行工作線程 = {num_workers}")
    print(f"    - 負載比 M/N = {load_ratio:.2f}")
    print(f"    - 自適應微批次大小 = {micro_batch_size}")
    print(f"    - 總任務數 = {num_tasks}")
    print("=" * 70)
    
    start_time = time.time()
    
    # 預分配結果陣列
    results_array = np.empty((num_samples, 3), dtype=np.float64)
    
    # 滑動窗口任務提交
    completed_samples = 0
    max_pending = num_workers * 2  # 保持適量任務在佇列
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        active_futures = {}
        current_idx = 0
        remaining_samples = num_samples
        
        # 初始提交一批任務
        while len(active_futures) < max_pending and remaining_samples > 0:
            count = min(micro_batch_size, remaining_samples)
            args = (M, N, I_max, current_idx, count, results_array)
            future = executor.submit(_micro_batch_worker, args)
            active_futures[future] = count
            current_idx += count
            remaining_samples -= count
        
        # 使用 tqdm 顯示進度
        with tqdm(total=num_samples, desc="模擬進度", unit="樣本", 
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,.0f}/{total:,.0f} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
            
            while active_futures:
                # 等待任意任務完成
                done, _ = wait(active_futures.keys(), return_when=FIRST_COMPLETED)
                
                for future in done:
                    batch_count = active_futures.pop(future)
                    future.result()  # 確認完成
                    
                    # 更新進度
                    completed_samples += batch_count
                    pbar.update(batch_count)
                    
                    # 提交新任務填補空缺
                    if remaining_samples > 0:
                        count = min(micro_batch_size, remaining_samples)
                        args = (M, N, I_max, current_idx, count, results_array)
                        new_future = executor.submit(_micro_batch_worker, args)
                        active_futures[new_future] = count
                        current_idx += count
                        remaining_samples -= count
    
    elapsed_time = time.time() - start_time
    samples_per_sec = num_samples / elapsed_time
    
    print("=" * 70)
    print(f"  模擬完成!")
    print(f"    - 總耗時: {elapsed_time:.2f} 秒")
    print(f"    - 平均速度: {samples_per_sec:,.0f} 樣本/秒")
    print(f"    - 記憶體優化: 預分配 {num_samples * 3 * 8 / 1024 / 1024:.1f} MB")
    print("=" * 70)
    
    return results_array

