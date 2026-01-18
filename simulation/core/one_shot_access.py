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
# 如果調用函數時沒有提供 rng，將使用此全域實例，避免重複創建開銷
_default_rng = np.random.default_rng()


def simulate_one_shot_access_single_ac(M: int, N: int, rng: np.random.Generator = None):
    """
    模擬一次 One-Shot Random Access（單個 AC）- 核心函數
    
    Args:
        M: 嘗試接入的設備數量 (UEs)
        N: 可用的 RAO 數量 (Preamble pool size)
        rng: numpy Generator（可選，用於並行計算確保獨立性）
    
    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
    """
    # 1. 如果沒有提供 rng，使用模組級默認 rng
    if rng is None:
        rng = _default_rng
    
    # 2. 隨機選擇過程 (Random Access)
    # 每個設備 (M) 從 N 個可用的資源 (RAO) 中均勻隨機選擇一個
    # 生成一個長度為 M 的陣列，每個元素代表該設備選擇的 RAO 索引 (0 到 N-1)
    choices = rng.integers(0, N, size=M)
    
    # 3. 統計每個 RAO 被選中的次數
    # minlength=N 確保即使後面的一些 RAO 沒被選中，統計數組長度也保持為 N
    rao_usage = np.bincount(choices, minlength=N)
    
    # 4. 計算結果分類
    # 成功 (Success): 只有 1 個設備選擇該 RAO
    success_raos = np.sum(rao_usage == 1)
    
    # 碰撞 (Collision): 有 2 個或更多設備選擇該 RAO
    collision_raos = np.sum(rao_usage >= 2)
    
    # 空閒 (Idle): 沒有任何設備選擇該 RAO
    idle_raos = np.sum(rao_usage == 0)
    
    return success_raos, collision_raos, idle_raos


def simulate_group_paging_single_sample(M: int, N: int, I_max: int, rng=None):
    """
    模擬一次完整的群組尋呼過程（多個 AC）
    Group Paging 包含多個連續的 Access Cycle (AC)，直到所有設備成功接入或達到最大週期數 I_max
    
    Args:
        M: 初始設備數 (Total UEs)
        N: 每個 AC 的 RAO 數 (Preamble pool size per cycle)
        I_max: 最大 AC 數 (Maximum number of Access Cycles)
        rng: numpy Generator（可選，用於並行計算）
    
    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
    """
    remaining_devices = M      # 當前尚未成功接入的設備數
    success_count = 0          # 累積成功接入的設備總數
    success_delay_sum = 0      # 累積成功接入的延遲總和 (用於計算平均延遲)
    total_collision_count = 0  # 累積發生的碰撞次數 (以 RAO 為單位)
    
    # 循環執行每一個 Access Cycle (AC)，從 1 到 I_max
    for ac_index in range(1, I_max + 1):
        # 如果所有設備都已經成功接入，提前結束循環
        if remaining_devices == 0:
            break
        
        # 調用核心函數模擬當前 AC 的競爭情況
        # 傳入當前剩餘的設備數作為本次嘗試接入的數量
        success_raos, collision_raos, _ = simulate_one_shot_access_single_ac(
            remaining_devices, N, rng
        )
        
        # 更新統計數據
        success_count += success_raos
        # 延遲計算：當前 AC 成功的設備，其延遲為當前 AC 索引 (ac_index)
        success_delay_sum += success_raos * ac_index
        total_collision_count += collision_raos
        
        # 減少剩餘設備數，只有失敗的設備會進入下一個 AC
        remaining_devices -= success_raos
    
    # 計算最終性能指標
    # 1. 接入成功率 (Access Success Probability)
    access_success_prob = success_count / M if M > 0 else 0.0
    
    # 2. 平均接入延遲 (Mean Access Delay)
    mean_access_delay = success_delay_sum / success_count if success_count > 0 else -1.0
    
    # 3. 碰撞概率 (Collision Probability)
    # 定義為：總碰撞 RAO 數 / 總可用 RAO 數 (I_max * N)
    # 注意：這裡的分母是整個過程理論上提供的總資源，而不僅僅是實際使用的 AC
    total_rao_count = I_max * N
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0
    
    return access_success_prob, mean_access_delay, collision_prob


def _simulate_batch_worker(M: int, N: int, I_max: int, batch_size: int, seed: int):
    """
    批量處理工作函數：在單個進程中執行多個樣本模擬
    
    設計目的：
    1. 減少進程間通信 (IPC) 開銷：傳遞一次參數，執行多次模擬
    2. 確保隨機性獨立：每個 Worker 使用獨立的 Seed 初始化 RNG
    """
    # 使用傳入的種子初始化獨立的 RNG，確保並行安全
    rng = np.random.default_rng(seed)
    
    # 預分配結果數組，避免動態擴展內存
    # Shape: [batch_size, 3] -> 存放 (ASP, Delay, CP)
    batch_results = np.empty((batch_size, 3), dtype=np.float64)
    
    # 執行 batch_size 次獨立模擬
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
    
    使用 ProcessPoolExecutor 進行並行計算，將大量樣本分塊 (Chunk) 分配給多個核心。
    
    Args:
        M: 初始設備總數
        N: 每個 AC 的 RAO 數量
        I_max: 最大接入周期數
        num_samples: 模擬樣本數 (通常很大，如 10^5 ~ 10^7)
        num_workers: 並行工作進程數 (-1 表示使用所有 CPU 核心)
    
    Returns:
        np.ndarray: Shape [num_samples, 3] 的結果矩陣，包含所有樣本的模擬結果
    """
    # 確定使用的 CPU 核心數
    if num_workers == -1:
        num_workers = os.cpu_count() or 1
    
    # 分塊策略 (Chunking Strategy)
    # 將總樣本數分成比核心數稍多的塊 (4倍)，有助於負載均衡 (Load Balancing)
    # 避免某些任務過慢導致 CPU 空閒
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
        # 生成高質量的獨立種子序列 (SeedSequence)
        # 這是 Numpy 推薦的並行隨機數生成方式，確保不同進程間的隨機流不相關
        child_seeds = np.random.SeedSequence().spawn(num_chunks)
        
        # 提交任務
        futures = []
        for i in range(num_chunks):
            # 計算當前塊的大小 (處理餘數)
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            if chunk_size == 0:
                continue
            
            # 獲取對應的種子狀態
            seed = child_seeds[i].generate_state(1)[0]
            
            # 提交非同步任務
            futures.append(executor.submit(_simulate_batch_worker, M, N, I_max, chunk_size, seed))
        
        # 收集結果並顯示進度條
        with tqdm(total=num_samples, desc="模擬進度", unit="樣本",
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,}/{total:,} [{elapsed}<{remaining}]') as pbar:
            for future in as_completed(futures):
                batch_res = future.result()
                all_results.append(batch_res)
                pbar.update(batch_res.shape[0])

    # 將所有批次的結果合併為一個大數組
    final_results = np.vstack(all_results)
    elapsed = time.time() - start_time
    
    print("=" * 70)
    print(f"  完成! 耗時: {elapsed:.2f}s | 速度: {num_samples/elapsed:,.0f} 樣本/秒")
    print("=" * 70)
    
    return final_results

