"""
One-Shot Random Access 模擬模組

模擬完整的 One-Shot Random Access 過程

架構層次：
1. simulate_one_shot_access_single_ac - 單次 AC 模擬（核心）
2. simulate_group_paging_single_sample - 單次完整群組尋呼（多個 AC）
3. simulate_group_paging_multi_samples - 批量多樣本並行模擬（10^7 級別）

優化策略：
1. Batch Processing - 減少 IPC 開銷
2. 獨立 RNG - 確保並行正確性
3. 預分配 numpy array - 減少記憶體碎片

注意：一旦此文件被更新，請同步更新項目根目錄 README.md
"""

import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm


# 模組級別的默認 RNG（用於非並行場景）
_default_rng = np.random.default_rng()


def simulate_one_shot_access_single_ac(M: int, N: int, rng: np.random.Generator = None):
    """
    模擬一次 One-Shot Random Access（單個 AC）- 核心函數
    
    Args:
        M: 嘗試接入的設備數量
        N: 可用的 RAO 數量
        rng: numpy Generator（可選，用於並行計算）
    
    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
    """
    if rng is None:
        rng = _default_rng
    
    choices = rng.integers(0, N, size=M)
    rao_usage = np.bincount(choices, minlength=N)
    
    success_raos = np.sum(rao_usage == 1)
    collision_raos = np.sum(rao_usage >= 2)
    idle_raos = np.sum(rao_usage == 0)
    
    return success_raos, collision_raos, idle_raos


def simulate_group_paging_single_sample(M: int, N: int, I_max: int, rng=None):
    """
    模擬一次完整的群組尋呼過程（多個 AC）
    
    Args:
        M: 初始設備數
        N: 每個 AC 的 RAO 數
        I_max: 最大 AC 數
        rng: numpy Generator（可選，用於並行計算）
    
    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
    """
    remaining_devices = M
    success_count = 0
    success_delay_sum = 0
    total_collision_count = 0
    
    for ac_index in range(1, I_max + 1):
        if remaining_devices == 0:
            break
        
        success_raos, collision_raos, _ = simulate_one_shot_access_single_ac(
            remaining_devices, N, rng
        )
        
        success_count += success_raos
        success_delay_sum += success_raos * ac_index
        total_collision_count += collision_raos
        remaining_devices -= success_raos
    
    # 計算指標
    access_success_prob = success_count / M if M > 0 else 0.0
    mean_access_delay = success_delay_sum / success_count if success_count > 0 else -1.0
    total_rao_count = I_max * N
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0
    
    return access_success_prob, mean_access_delay, collision_prob


def _simulate_batch_worker(M: int, N: int, I_max: int, batch_size: int, seed: int):
    """批量處理：在單個進程中執行多個樣本模擬"""
    rng = np.random.default_rng(seed)
    batch_results = np.empty((batch_size, 3), dtype=np.float64)
    
    for i in range(batch_size):
        result = simulate_group_paging_single_sample(M, N, I_max, rng)
        batch_results[i, 0] = result[0]
        batch_results[i, 1] = result[1]
        batch_results[i, 2] = result[2]
    
    return batch_results


def simulate_group_paging_multi_samples(M: int, N: int, I_max: int, num_samples: int, 
                                        num_workers: int):
    """
    高效並行多樣本模擬（Batch Optimization）
    
    Args:
        M: 初始設備總數
        N: 每個 AC 的 RAO 數量
        I_max: 最大接入周期數
        num_samples: 模擬樣本數
        num_workers: 並行工作進程數 (-1 表示使用所有 CPU 核心)
    
    Returns:
        np.ndarray: Shape [num_samples, 3] 的結果矩陣
    """
    if num_workers == -1:
        num_workers = os.cpu_count() or 1
    
    # 分塊策略：CPU核心數 * 4，確保負載均衡
    num_chunks = num_workers * 4
    base_chunk_size = num_samples // num_chunks
    remainder = num_samples % num_chunks
    
    print("=" * 70)
    print("【Group Paging】高效並行模擬 (Batch Optimization)")
    print("=" * 70)
    print(f"  參數: M={M}, N={N}, I_max={I_max}")
    print(f"  樣本數: {num_samples:,} | 進程: {num_workers} | 分塊: {num_chunks}")
    print("=" * 70)
    
    start_time = time.time()
    all_results = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        # 生成獨立種子
        child_seeds = np.random.SeedSequence().spawn(num_chunks)
        
        # 提交任務
        futures = []
        for i in range(num_chunks):
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            if chunk_size == 0:
                continue
            seed = child_seeds[i].generate_state(1)[0]
            futures.append(executor.submit(_simulate_batch_worker, M, N, I_max, chunk_size, seed))
        
        # 收集結果
        with tqdm(total=num_samples, desc="模擬進度", unit="樣本",
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,}/{total:,} [{elapsed}<{remaining}]') as pbar:
            for future in as_completed(futures):
                batch_res = future.result()
                all_results.append(batch_res)
                pbar.update(batch_res.shape[0])

    final_results = np.vstack(all_results)
    elapsed = time.time() - start_time
    
    print("=" * 70)
    print(f"  完成! 耗時: {elapsed:.2f}s | 速度: {num_samples/elapsed:,.0f} 樣本/秒")
    print("=" * 70)
    
    return final_results

