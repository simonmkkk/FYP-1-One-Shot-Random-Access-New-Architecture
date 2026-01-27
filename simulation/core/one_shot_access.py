"""
============================================================================
one_shot_access - One-Shot Random Access 模擬引擎
============================================================================

此模組實現 One-Shot Random Access 的蒙特卡洛模擬。

模擬完整的 One-Shot Random Access 過程，包含三個層次：
1. simulate_one_shot_access_single_ac - 單次 AC 模擬（核心）
2. simulate_group_paging_single_sample - 單次完整群組尋呼（多個 AC）
3. simulate_group_paging_multi_samples - 批量多樣本並行模擬（10^7 級別）

優化策略：
1. Batch Processing - 減少 IPC 開銷
2. 獨立 RNG - 確保並行正確性
3. 預分配 numpy array - 減少記憶體碎片

Input: M（設備數）, N（RAO 數）, I_max（最大 AC 數）, num_samples
Output: 模擬結果數組 [num_samples, 3] -> (P_S, T_a, P_C)
Position: simulation core 的模擬引擎層

注意：一旦此文件被更新，請同步更新項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 標準庫導入
# ============================================================================
import os  # 作業系統介面，用於獲取 CPU 核心數
import time  # 計時模組，用於測量模擬耗時

# ============================================================================
# 第三方庫導入
# ============================================================================
import numpy as np  # NumPy 數值計算庫，用於向量化操作和隨機數生成
from concurrent.futures import ProcessPoolExecutor, as_completed  # 多進程並行執行器
from tqdm import tqdm  # 進度條顯示庫


# ============================================================================
# 模組級常數
# ============================================================================

# 模組級別的默認 RNG（用於非並行場景）
# 如果調用函數時沒有提供 rng，將使用此全域實例，避免重複創建開銷
_default_rng = np.random.default_rng()  # 預設隨機數生成器（模組級單例）


# ============================================================================
# 核心模擬函數
# ============================================================================

def simulate_one_shot_access_single_ac(M: int, N: int, rng: np.random.Generator = None):
    """
    模擬一次 One-Shot Random Access（單個 AC）- 核心函數
    
    此函數模擬單個 Access Cycle (AC) 中的隨機接入過程：
    1. M 個設備各自從 N 個 RAO 中均勻隨機選擇一個
    2. 統計每個 RAO 的使用情況
    3. 分類為成功（唯一選擇）、碰撞（多重選擇）、空閒（無選擇）
    
    Args:
        M: 嘗試接入的設備數量 (UEs)
        N: 可用的 RAO 數量 (Preamble pool size)
        rng: numpy Generator（可選，用於並行計算確保獨立性）
    
    Returns:
        tuple: (success_raos, collision_raos, idle_raos)
            - success_raos: 成功接入的 RAO 數（恰好 1 個設備選擇）
            - collision_raos: 發生碰撞的 RAO 數（≥2 個設備選擇）
            - idle_raos: 空閒的 RAO 數（0 個設備選擇）
    """
    # 參數說明（來源 + 是什麼）
    # - M: int（嘗試接入的設備數量）
    #   來源：上層 simulate_group_paging_single_sample 傳入，初始為總設備數，後續為剩餘設備數
    # - N: int（可用 RAO 數量 / Preamble pool size）
    #   來源：由 runner/main 通過 Config 傳入
    # - rng: np.random.Generator（隨機數生成器）
    #   來源：並行時由 worker 創建，非並行時使用模組級 _default_rng
    
    # ------------------------------------------------------------------------
    # 步驟 1：確定使用的隨機數生成器
    # ------------------------------------------------------------------------
    if rng is None:  # 如果沒有提供 rng
        rng = _default_rng  # 使用模組級默認 rng（非並行場景）
    
    # ------------------------------------------------------------------------
    # 步驟 2：隨機選擇過程 (Random Access)
    # ------------------------------------------------------------------------
    # 每個設備 (M) 從 N 個可用的資源 (RAO) 中均勻隨機選擇一個
    # 生成一個長度為 M 的陣列，每個元素代表該設備選擇的 RAO 索引 (0 到 N-1)
    choices = rng.integers(0, N, size=M)  # 向量化隨機選擇，O(M) 時間
    
    # ------------------------------------------------------------------------
    # 步驟 3：統計每個 RAO 被選中的次數
    # ------------------------------------------------------------------------
    # 使用 bincount 進行桶計數，統計每個 RAO 被多少設備選中
    # minlength=N 確保即使後面的一些 RAO 沒被選中，統計數組長度也保持為 N
    rao_usage = np.bincount(choices, minlength=N)  # O(M) 時間複雜度
    
    # ------------------------------------------------------------------------
    # 步驟 4：計算結果分類
    # ------------------------------------------------------------------------
    # 成功 (Success): 只有 1 個設備選擇該 RAO -> 該設備成功接入
    success_raos = np.sum(rao_usage == 1)  # 統計成功 RAO 數
    
    # 碰撞 (Collision): 有 2 個或更多設備選擇該 RAO -> 所有相關設備失敗
    collision_raos = np.sum(rao_usage >= 2)  # 統計碰撞 RAO 數
    
    # 空閒 (Idle): 沒有任何設備選擇該 RAO -> 資源浪費
    idle_raos = np.sum(rao_usage == 0)  # 統計空閒 RAO 數
    
    return success_raos, collision_raos, idle_raos  # 返回三元組結果


def simulate_group_paging_single_sample(M: int, N: int, I_max: int, rng=None):
    """
    模擬一次完整的群組尋呼過程（多個 AC）
    
    Group Paging 包含多個連續的 Access Cycle (AC)：
    - 每個 AC 中，剩餘設備嘗試接入
    - 成功的設備退出，失敗的設備進入下一個 AC
    - 直到所有設備成功接入或達到最大週期數 I_max
    
    Args:
        M: 初始設備數 (Total UEs)
        N: 每個 AC 的 RAO 數 (Preamble pool size per cycle)
        I_max: 最大 AC 數 (Maximum number of Access Cycles)
        rng: numpy Generator（可選，用於並行計算）
    
    Returns:
        tuple: (access_success_prob, mean_access_delay, collision_prob)
            - access_success_prob: 接入成功率 P_S = 成功設備數 / 總設備數
            - mean_access_delay: 平均接入延遲 T_a = 成功延遲總和 / 成功設備數
            - collision_prob: 碰撞概率 P_C = 碰撞 RAO 數 / 總 RAO 數
    """
    # 參數說明（來源 + 是什麼）
    # - M: int（初始設備總數）
    #   來源：由 Config.M 傳入
    # - N: int（每個 AC 的 RAO 數）
    #   來源：N-scan 時由 runner 動態傳入
    # - I_max: int（最大 AC 數，限制重試次數）
    #   來源：由 Config.I_max 傳入
    # - rng: np.random.Generator（隨機數生成器）
    #   來源：batch_worker 創建後傳入
    
    # ------------------------------------------------------------------------
    # 初始化狀態變數
    # ------------------------------------------------------------------------
    remaining_devices = M      # 當前尚未成功接入的設備數
    success_count = 0          # 累積成功接入的設備總數
    success_delay_sum = 0      # 累積成功接入的延遲總和（用於計算平均延遲）
    total_collision_count = 0  # 累積發生的碰撞次數（以 RAO 為單位）
    
    # ------------------------------------------------------------------------
    # 主循環：執行每一個 Access Cycle (AC)
    # ------------------------------------------------------------------------
    for ac_index in range(1, I_max + 1):  # AC 索引從 1 到 I_max
        # 如果所有設備都已經成功接入，提前結束循環
        if remaining_devices == 0:  # 提前終止條件
            break
        
        # 調用核心函數模擬當前 AC 的競爭情況
        # 傳入當前剩餘的設備數作為本次嘗試接入的數量
        success_raos, collision_raos, _ = simulate_one_shot_access_single_ac(
            remaining_devices, N, rng  # 剩餘設備爭奪 N 個 RAO
        )
        
        # 更新統計數據
        success_count += success_raos  # 累加成功設備數
        # 延遲計算：當前 AC 成功的設備，其延遲為當前 AC 索引 (ac_index)
        success_delay_sum += success_raos * ac_index  # 累加加權延遲
        total_collision_count += collision_raos  # 累加碰撞 RAO 數
        
        # 減少剩餘設備數，只有失敗的設備會進入下一個 AC
        remaining_devices -= success_raos  # 成功設備退出
    
    # ------------------------------------------------------------------------
    # 計算最終性能指標
    # ------------------------------------------------------------------------
    # 1. 接入成功率 (Access Success Probability)
    # P_S = 成功接入的設備數 / 總設備數
    access_success_prob = success_count / M if M > 0 else 0.0  # 避免除零
    
    # 2. 平均接入延遲 (Mean Access Delay)
    # T_a = 成功延遲總和 / 成功設備數
    # 延遲單位為 AC 數（即第幾個 AC 成功）
    mean_access_delay = success_delay_sum / success_count if success_count > 0 else -1.0  # -1 表示無有效延遲
    
    # 3. 碰撞概率 (Collision Probability)
    # P_C = 總碰撞 RAO 數 / 總可用 RAO 數
    # 分母是整個過程理論上提供的總資源 (I_max * N)，而不僅僅是實際使用的 AC
    total_rao_count = I_max * N  # 總 RAO 資源
    collision_prob = total_collision_count / total_rao_count if total_rao_count > 0 else 0.0  # 避免除零
    
    return access_success_prob, mean_access_delay, collision_prob  # 返回三指標


# ============================================================================
# 並行處理 Worker 函數
# ============================================================================

def _simulate_batch_worker(M: int, N: int, I_max: int, batch_size: int, seed: int):
    """
    批量處理工作函數：在單個進程中執行多個樣本模擬
    
    此函數在子進程中執行，負責處理一個批次的模擬任務。
    設計目的：
    1. 減少進程間通信 (IPC) 開銷：傳遞一次參數，執行多次模擬
    2. 確保隨機性獨立：每個 Worker 使用獨立的 Seed 初始化 RNG
    
    Args:
        M: 初始設備數量
        N: RAO 數量
        I_max: 最大 AC 數
        batch_size: 本批次要執行的模擬次數
        seed: 隨機種子（由 SeedSequence 生成，確保獨立性）
    
    Returns:
        np.ndarray: Shape [batch_size, 3] 的結果矩陣
            - 列 0: Access Success Probability (P_S)
            - 列 1: Mean Access Delay (T_a)
            - 列 2: Collision Probability (P_C)
    """
    # 參數說明（來源 + 是什麼）
    # - M/N/I_max: 模擬參數，由主進程傳入
    # - batch_size: int（本批次樣本數）
    #   來源：主進程根據 chunk 分配策略計算
    # - seed: int（隨機種子）
    #   來源：主進程使用 SeedSequence.spawn() 生成獨立種子
    
    # 使用傳入的種子初始化獨立的 RNG，確保並行安全
    rng = np.random.default_rng(seed)  # 創建進程專屬 RNG
    
    # 預分配結果數組，避免動態擴展內存
    # Shape: [batch_size, 3] -> 存放 (P_S, T_a, P_C)
    batch_results = np.empty((batch_size, 3), dtype=np.float64)  # 預分配記憶體
    
    # 執行 batch_size 次獨立模擬
    for i in range(batch_size):  # 逐樣本模擬
        result = simulate_group_paging_single_sample(M, N, I_max, rng)  # 單次完整模擬
        batch_results[i, 0] = result[0]  # P_S
        batch_results[i, 1] = result[1]  # T_a
        batch_results[i, 2] = result[2]  # P_C
    
    return batch_results  # 返回批次結果


# ============================================================================
# 高效並行多樣本模擬
# ============================================================================

def simulate_group_paging_multi_samples(M: int, N: int, I_max: int, num_samples: int, 
                                        num_workers: int):
    """
    高效並行多樣本模擬（Batch Optimization）
    
    使用 ProcessPoolExecutor 進行並行計算，將大量樣本分塊 (Chunk) 分配給多個核心。
    適用於 10^5 ~ 10^7 級別的大規模蒙特卡洛模擬。
    
    並行策略：
    1. 將總樣本分成 num_workers * 4 個塊（有助於負載均衡）
    2. 使用 SeedSequence 生成獨立種子（確保隨機性正確）
    3. 異步提交任務，使用進度條跟踪完成情況
    
    Args:
        M: 初始設備總數
        N: 每個 AC 的 RAO 數量
        I_max: 最大接入周期數
        num_samples: 模擬樣本數（通常很大，如 10^5 ~ 10^7）
        num_workers: 並行工作進程數（-1 表示使用所有 CPU 核心）
    
    Returns:
        np.ndarray: Shape [num_samples, 3] 的結果矩陣
            - 列 0: Access Success Probability (P_S)
            - 列 1: Mean Access Delay (T_a)
            - 列 2: Collision Probability (P_C)
    """
    # 參數說明（來源 + 是什麼）
    # - M/N/I_max: 模擬參數，由 Config 或 runner 傳入
    # - num_samples: int（總模擬樣本數）
    #   來源：Config.num_samples
    # - num_workers: int（並行進程數）
    #   來源：Config.num_workers（-1 表示自動）
    
    # ------------------------------------------------------------------------
    # 步驟 1：確定使用的 CPU 核心數
    # ------------------------------------------------------------------------
    if num_workers == -1:  # 自動模式
        num_workers = os.cpu_count() or 1  # 使用所有可用核心，至少 1 個
    
    # ------------------------------------------------------------------------
    # 步驟 2：分塊策略 (Chunking Strategy)
    # ------------------------------------------------------------------------
    # 將總樣本數分成比核心數稍多的塊 (4倍)，有助於負載均衡 (Load Balancing)
    # 避免某些任務過慢導致 CPU 空閒
    num_chunks = num_workers * 4  # 塊數 = 核心數 × 4
    base_chunk_size = num_samples // num_chunks  # 基礎塊大小
    remainder = num_samples % num_chunks  # 餘數（前 remainder 個塊多 1 個樣本）
    
    # ------------------------------------------------------------------------
    # 步驟 3：打印模擬信息
    # ------------------------------------------------------------------------
    print("=" * 70)
    print("【Group Paging】高效並行模擬 (Batch Optimization)")
    print("=" * 70)
    print(f"  參數: M={M}, N={N}, I_max={I_max}")
    print(f"  樣本數: {num_samples:,} | 進程: {num_workers} | 分塊: {num_chunks}")
    print("=" * 70)
    
    start_time = time.time()  # 記錄開始時間
    all_results = []  # 收集所有批次結果
    
    # ------------------------------------------------------------------------
    # 步驟 4：並行執行
    # ------------------------------------------------------------------------
    with ProcessPoolExecutor(max_workers=num_workers) as executor:  # 創建進程池
        # 生成高質量的獨立種子序列 (SeedSequence)
        # 這是 NumPy 推薦的並行隨機數生成方式，確保不同進程間的隨機流不相關
        child_seeds = np.random.SeedSequence().spawn(num_chunks)  # 生成 num_chunks 個獨立種子
        
        # 提交任務
        futures = []  # 任務句柄列表
        for i in range(num_chunks):  # 逐塊提交
            # 計算當前塊的大小（處理餘數：前 remainder 個塊多 1 個樣本）
            chunk_size = base_chunk_size + (1 if i < remainder else 0)
            if chunk_size == 0:  # 跳過空塊
                continue
            
            # 獲取對應的種子狀態
            seed = child_seeds[i].generate_state(1)[0]  # 生成實際種子值
            
            # 提交非同步任務
            futures.append(executor.submit(
                _simulate_batch_worker, M, N, I_max, chunk_size, seed
            ))  # 提交 batch worker 任務
        
        # 收集結果並顯示進度條
        with tqdm(total=num_samples, desc="模擬進度", unit="樣本",
                  bar_format='{desc}: {percentage:3.0f}%|{bar}| {n:,}/{total:,} [{elapsed}<{remaining}]') as pbar:
            for future in as_completed(futures):  # 異步收集完成的任務
                batch_res = future.result()  # 獲取批次結果
                all_results.append(batch_res)  # 加入結果列表
                pbar.update(batch_res.shape[0])  # 更新進度條

    # ------------------------------------------------------------------------
    # 步驟 5：合併結果並輸出統計
    # ------------------------------------------------------------------------
    # 將所有批次的結果合併為一個大數組
    final_results = np.vstack(all_results)  # 垂直堆疊所有批次
    elapsed = time.time() - start_time  # 計算總耗時
    
    print("=" * 70)
    print(f"  完成! 耗時: {elapsed:.2f}s | 速度: {num_samples/elapsed:,.0f} 樣本/秒")
    print("=" * 70)
    
    return final_results  # 返回 [num_samples, 3] 的結果矩陣


# ============================================================================
# 模組導出
# ============================================================================

__all__ = [
    "simulate_one_shot_access_single_ac",  # 單次 AC 模擬
    "simulate_group_paging_single_sample",  # 單次完整群組尋呼
    "simulate_group_paging_multi_samples",  # 批量並行模擬
]
