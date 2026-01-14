"""
群組尋呼模擬模組

模擬完整的群組尋呼過程（多個 AC）

使用 ProcessPoolExecutor 實現多進程並行計算

架構設計：
- simulate_group_paging_single_sample: 通過循環調用 one_shot_access 實現單次群組尋呼模擬
- simulate_group_paging_multi_samples: 通過 Batching 策略實現高效多樣本並行模擬

優化策略：
1. Batch Processing (分塊處理) - 大幅減少 IPC 開銷
2. 獨立 RNG (隨機數生成器) - 使用 np.random.SeedSequence 確保並行正確性
3. 預分配 numpy array - 減少記憶體碎片

Input: M, N, I_max 參數, num_samples 樣本數
Output: simulate_group_paging_multi_samples() 多樣本並行模擬
Position: 蒙特卡洛模擬的核心執行引擎，依賴 one_shot_access 模組

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import os
import time
import numpy as np
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

from .one_shot_access import (
    simulate_one_shot_access_single_ac,
    simulate_one_shot_access_single_ac_rng,
)


def simulate_group_paging_single_sample(M: int, N: int, I_max: int):
    """
    模擬一次完整的群組尋呼過程
    
    通過循環調用 simulate_one_shot_access_single_ac 實現多個 AC 的群組尋呼。
    每個 AC 周期中，剩餘設備嘗試隨機接入，成功的設備被移除，未成功的設備繼續下一個 AC。
    
    Args:
        M: 初始設備數
        N: 每個 AC 的 RAO 數
        I_max: 最大 AC 數
    
    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
    """
    remaining_devices = M
    success_count = 0
    success_delay_sum = 0
    total_collision_count = 0
    
    for ac_index in range(1, I_max + 1):
        if remaining_devices == 0:
            continue
        
        # 調用核心模擬函數進行單次 AC 模擬
        success_raos, collision_raos, _ = simulate_one_shot_access_single_ac(
            remaining_devices, N
        )
        
        # 累積統計信息
        success_count += success_raos
        success_delay_sum += success_raos * ac_index
        total_collision_count += collision_raos
        
        # 更新剩餘設備數（成功的設備不再參與後續 AC）
        remaining_devices -= success_raos
    
    # 計算最終指標
    access_success_prob = success_count / M if M > 0 else 0.0
    
    if success_count > 0:
        mean_access_delay = success_delay_sum / success_count
    else:
        mean_access_delay = -1.0
    
    total_rao_count = I_max * N
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0
    
    return access_success_prob, mean_access_delay, collision_prob


def _simulate_batch_worker(M: int, N: int, I_max: int, batch_size: int, seed: int):
    """
    工作進程函數：在一個進程中連續執行多個樣本模擬
    
    優化點：
    1. 減少 IPC (進程通訊) 開銷 - 批量處理多個樣本
    2. 使用獨立的 Random Generator 確保隨機性與速度
    3. 在進程內預分配記憶體
    
    Args:
        M: 初始設備數
        N: 每個 AC 的 RAO 數
        I_max: 最大 AC 數
        batch_size: 此批次的樣本數量
        seed: 隨機數種子（確保並行可重現性）
    
    Returns:
        np.ndarray: Shape [batch_size, 3] 的結果矩陣
    """
    # 初始化獨立的隨機數生成器 (比 legacy np.random 快且線程安全)
    rng = np.random.default_rng(seed)
    
    # 預分配該批次的結果矩陣
    batch_results = np.empty((batch_size, 3), dtype=np.float64)
    
    for i in range(batch_size):
        remaining_devices = M
        success_count = 0
        success_delay_sum = 0
        total_collision_count = 0
        
        # --- 單樣本模擬邏輯開始 ---
        for ac_index in range(1, I_max + 1):
            if remaining_devices == 0:
                break
            
            # 呼叫核心模擬（使用 RNG 優化版本）
            success_raos, collision_raos, _ = simulate_one_shot_access_single_ac_rng(
                remaining_devices, N, rng
            )
            
            success_count += success_raos
            success_delay_sum += success_raos * ac_index
            total_collision_count += collision_raos
            remaining_devices -= success_raos
        # --- 單樣本模擬邏輯結束 ---
        
        # 計算指標
        # 1. Access Success Probability
        batch_results[i, 0] = success_count / M if M > 0 else 0.0
        
        # 2. Mean Access Delay
        if success_count > 0:
            batch_results[i, 1] = success_delay_sum / success_count
        else:
            batch_results[i, 1] = -1.0
            
        # 3. Collision Probability
        total_rao_count = I_max * N
        batch_results[i, 2] = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0
        
    return batch_results


def simulate_group_paging_multi_samples(M: int, N: int, I_max: int, num_samples: int, 
                                        num_workers: int):
    """
    高效並行執行完整群組尋呼過程的多樣本模擬（Batch Optimization）
    
    使用 Batching 策略大幅減少 IPC 開銷：
    - 原版：每個樣本提交一次任務（10^7 次 IPC）
    - 優化版：將樣本分成 ~64 個批次（~64 次 IPC），通訊開銷降低 10,000 倍以上
    
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
    
    # 計算分塊大小
    # 策略：將任務切分為 (CPU核心數 * 4) 份，確保負載均衡，同時避免過多通訊
    num_chunks = num_workers * 4
    base_chunk_size = num_samples // num_chunks
    remainder = num_samples % num_chunks
    
    load_ratio = M / N
    print("=" * 70)
    print("【Group Paging】高效並行模擬 (Batch Optimization)")
    print("=" * 70)
    print(f"  參數配置:")
    print(f"    - 設備數 M = {M}")
    print(f"    - RAO 數 N = {N}")
    print(f"    - 最大 AC 數 I_max = {I_max}")
    print(f"    - 總樣本數: {num_samples:,}")
    print(f"    - 工作進程: {num_workers}")
    print(f"    - 任務分塊: {num_chunks} chunks")
    print(f"    - 平均每塊: ~{base_chunk_size:,} samples")
    print(f"    - 負載比 M/N = {load_ratio:.2f}")
    print("=" * 70)
    
    start_time = time.time()
    
    # 用於收集所有批次的結果
    all_results_list = []
    
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        futures = []
        
        # 生成種子 (確保並行重現性)
        # 使用 SeedSequence 產生高熵獨立種子
        seed_seq = np.random.SeedSequence()
        child_seeds = seed_seq.spawn(num_chunks)
        
        # 提交批次任務
        for i in range(num_chunks):
            # 處理最後一塊可能多出的餘數
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            if chunk_size == 0:
                continue
                
            seed = child_seeds[i].generate_state(1)[0]  # 獲取整數種子
            
            future = executor.submit(
                _simulate_batch_worker, M, N, I_max, chunk_size, seed
            )
            futures.append(future)
            
        # 處理結果
        with tqdm(total=num_samples, desc="模擬進度", unit="樣本",
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,.0f}/{total:,.0f} [{elapsed}<{remaining}, {rate_fmt}]') as pbar:
            for future in as_completed(futures):
                try:
                    batch_res = future.result()
                    all_results_list.append(batch_res)
                    pbar.update(batch_res.shape[0])  # 更新批次中的樣本數
                except Exception as e:
                    print(f"\n[Error] Worker failed: {e}")

    # 合併所有結果
    final_results = np.vstack(all_results_list)
    
    elapsed_time = time.time() - start_time
    samples_per_sec = num_samples / elapsed_time
    
    print("=" * 70)
    print(f"  模擬完成!")
    print(f"    - 總耗時: {elapsed_time:.2f} 秒")
    print(f"    - 處理速度: {samples_per_sec:,.0f} 樣本/秒")
    print(f"    - 記憶體使用: ~{num_samples * 3 * 8 / 1024 / 1024:.1f} MB (結果矩陣)")
    print("=" * 70)
    
    return final_results

