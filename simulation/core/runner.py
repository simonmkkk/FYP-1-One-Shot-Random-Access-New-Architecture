"""
============================================================================
runner - 並行執行與實驗管理
============================================================================

此模組提供 One-Shot Random Access 模擬的執行管理功能：
1. run_single_n_simulation: 執行單個 N 值的模擬
2. run_n_scan: 執行 N 值掃描（順序執行，內部並行）
3. run_experiment: 統一實驗入口（載入 YAML、執行掃描、保存 CSV）

設計理念：
- 使用 ProcessPoolExecutor 進行多進程並行
- 調用 one_shot_access 模組的模擬函數
- 參考 FYP-2 的架構設計

Input: Config 配置物件、YAML 配置文件
Output: List[SimulationResult]、CSV 文件
Position: simulation core 的執行層

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 標準庫導入
# ============================================================================
from __future__ import annotations  # 啟用延遲類型註解評估

import csv  # CSV 文件讀寫模組
import gc  # 垃圾回收模組，用於釋放內存
import os  # 作業系統介面，用於獲取 CPU 核心數
import time  # 計時模組，用於測量耗時
from concurrent.futures import ProcessPoolExecutor, as_completed  # 多進程並行執行器
from datetime import datetime  # 日期時間處理，用於生成時間戳
from pathlib import Path  # 物件導向的路徑處理
from typing import List, Literal, Sequence, Tuple  # 類型提示工具

import yaml  # YAML 文件解析庫

# ============================================================================
# 可選依賴：tqdm 進度條
# ============================================================================
try:
    from tqdm import tqdm  # 導入進度條庫
    HAS_TQDM = True  # 標記：有 tqdm 可用
except ImportError:
    tqdm = None  # tqdm 不可用
    HAS_TQDM = False  # 標記：無 tqdm

# ============================================================================
# 本地模組導入
# ============================================================================
from simulation.core.config import Config  # 配置類
from simulation.core.metrics import SimulationResult, calculate_performance_metrics  # 結果類和統計函數
from simulation.core.one_shot_access import simulate_group_paging_multi_samples  # 並行模擬函數


# ============================================================================
# 路徑常數
# ============================================================================

# 專案根目錄：從當前文件向上三級
# runner.py -> core/ -> simulation/ -> 專案根目錄
PROJECT_ROOT = Path(__file__).resolve().parents[2]  # 專案根目錄

# 模擬結果保存的根目錄
SIM_RESULT_ROOT = PROJECT_ROOT / "result" / "simulation"  # CSV 輸出根目錄


# ============================================================================
# 單點模擬函數
# ============================================================================

def run_single_n_simulation(cfg: Config, n_value: int) -> SimulationResult:
    """
    執行單個 N 值的模擬
    
    此函數對指定的 N 值執行蒙特卡洛模擬，返回結構化的結果。
    內部調用 simulate_group_paging_multi_samples 進行並行計算。
    
    Args:
        cfg: 模擬配置，包含 M、I_max、num_samples、num_workers 等參數
        n_value: N 值（RAO 數量）
        
    Returns:
        SimulationResult: 包含 P_S、T_a、P_C 均值和置信區間的結果
    """
    # 參數說明（來源 + 是什麼）
    # - cfg: Config（模擬配置物件）
    #   來源：run_n_scan() 或 run_experiment() 傳入
    # - n_value: int（當前掃描的 N 值）
    #   來源：run_n_scan() 的迴圈變數
    
    # ------------------------------------------------------------------------
    # 步驟 1：執行並行模擬
    # ------------------------------------------------------------------------
    results_array = simulate_group_paging_multi_samples(
        M=cfg.M,  # 初始設備數量
        N=n_value,  # 當前 N 值
        I_max=cfg.I_max,  # 最大 AC 數
        num_samples=cfg.num_samples,  # 模擬樣本數
        num_workers=cfg.num_workers,  # 並行進程數
    )  # 返回 [num_samples, 3] 的結果矩陣
    
    # ------------------------------------------------------------------------
    # 步驟 2：計算統計指標
    # ------------------------------------------------------------------------
    means, cis = calculate_performance_metrics(results_array)  # 計算均值和置信區間
    mean_ps, mean_ta, mean_pc = means  # 解包均值
    ci_ps, ci_ta, ci_pc = cis  # 解包置信區間
    
    # ------------------------------------------------------------------------
    # 步驟 3：釋放內存
    # ------------------------------------------------------------------------
    del results_array  # 釋放大型結果陣列
    gc.collect()  # 強制垃圾回收
    
    # ------------------------------------------------------------------------
    # 步驟 4：組裝並返回結果
    # ------------------------------------------------------------------------
    return SimulationResult(
        N=n_value,  # RAO 數量
        M=cfg.M,  # 初始設備數量
        I_max=cfg.I_max,  # 最大 AC 數
        num_samples=cfg.num_samples,  # 模擬樣本數
        mean_ps=mean_ps,  # 平均接入成功率
        mean_ta=mean_ta,  # 平均接入延遲
        mean_pc=mean_pc,  # 平均碰撞概率
        ci_ps=ci_ps,  # P_S 置信區間
        ci_ta=ci_ta,  # T_a 置信區間
        ci_pc=ci_pc,  # P_C 置信區間
    )


# ============================================================================
# 並行掃描函數
# ============================================================================

def run_n_scan(
    cfg: Config,
    n_values: Sequence[int] | None = None,
) -> List[SimulationResult]:
    """
    執行 N 值掃描模擬
    
    對每個 N 值執行蒙特卡洛模擬，返回所有結果。
    注意：由於 simulate_group_paging_multi_samples 內部已使用 ProcessPoolExecutor，
    這裡採用順序執行，避免嵌套並行。
    
    Args:
        cfg: 基礎模擬配置
        n_values: 要掃描的 N 值序列（None 則使用 cfg.n_range）
        
    Returns:
        List[SimulationResult]: 每個 N 值的模擬結果列表
    """
    # 確定 N 值列表
    if n_values is None:
        n_values = cfg.n_range
    
    print("=" * 70)
    print("【N-scan】One-Shot Random Access 模擬")
    print("=" * 70)
    print(f"  參數: M={cfg.M}, I_max={cfg.I_max}")
    print(f"  N 值範圍: {list(n_values)}")
    print(f"  樣本數: {cfg.num_samples:,}")
    print("=" * 70)
    
    results: List[SimulationResult] = []
    
    start_time = time.time()
    
    for n in n_values:
        print(f"\n正在模擬 N={n}...")
        result = run_single_n_simulation(cfg, n)
        results.append(result)
        print(f"  結果: P_S={result.mean_ps:.6f}, T_a={result.mean_ta:.4f}, P_C={result.mean_pc:.6f}")
    
    elapsed = time.time() - start_time
    
    print("\n" + "=" * 70)
    print(f"  完成! 總耗時: {elapsed:.2f}s")
    print("=" * 70)
    
    return results


# ============================================================================
# CSV 保存函數
# ============================================================================

# CSV 欄位定義
CSV_FIELDNAMES = [
    "N",              # RAO 數量
    "M",              # 初始設備數量
    "I_max",          # 最大 Access Cycle 數
    "P_S",            # 接入成功率
    "T_a",            # 平均接入延遲
    "P_C",            # 碰撞概率
    "CI_P_S",         # P_S 置信區間
    "CI_T_a",         # T_a 置信區間
    "CI_P_C",         # P_C 置信區間
    "num_samples",    # 模擬樣本數
]


def save_results_to_csv(
    results: List[SimulationResult],
    output_path: Path,
) -> None:
    """
    將模擬結果保存到 CSV 文件
    
    Args:
        results: 模擬結果列表
        output_path: 輸出文件路徑
    """
    # 確保輸出目錄存在
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()
        
        for result in results:
            row = {
                "N": result.N,
                "M": result.M,
                "I_max": result.I_max,
                "P_S": result.mean_ps,
                "T_a": result.mean_ta,
                "P_C": result.mean_pc,
                "CI_P_S": result.ci_ps,
                "CI_T_a": result.ci_ta,
                "CI_P_C": result.ci_pc,
                "num_samples": result.num_samples,
            }
            writer.writerow(row)
    
    print(f"✅ Results saved to: {output_path}")


# ============================================================================
# 統一實驗入口
# ============================================================================

def run_experiment(
    config_path: Path | str,
) -> List[SimulationResult]:
    """
    統一實驗執行器
    
    整合了模擬腳本的共同邏輯：
    1. 載入 YAML 配置文件
    2. 執行 N 掃描模擬
    3. 將結果保存到 CSV 文件
    
    Args:
        config_path: 實驗配置文件路徑（YAML 格式）
        
    Returns:
        List[SimulationResult]: 模擬結果列表
    """
    t0 = time.perf_counter()
    
    # 確保路徑為 Path 物件
    config_path = Path(config_path)
    
    # 載入配置
    cfg = Config.from_yaml_file(config_path)
    
    print(f"[config] M={cfg.M}, I_max={cfg.I_max}, num_samples={cfg.num_samples}")
    print(f"[config] N range: {cfg.n_range}")
    
    # 執行 N 掃描
    results = run_n_scan(cfg)
    
    # 生成時間戳
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # 確定輸出路徑
    output_dir = SIM_RESULT_ROOT / cfg.experiment_name / timestamp
    output_path = output_dir / f"{cfg.experiment_name}.csv"
    
    # 保存結果
    if cfg.save_csv:
        save_results_to_csv(results, output_path)
    
    elapsed = time.perf_counter() - t0
    print(f"⏱️ Experiment elapsed: {elapsed:.2f} s")
    
    return results


# ============================================================================
# 模組導出
# ============================================================================

__all__ = [
    # 路徑常數
    "PROJECT_ROOT",
    "SIM_RESULT_ROOT",
    
    # 模擬函數
    "run_single_n_simulation",
    "run_n_scan",
    
    # CSV 函數
    "save_results_to_csv",
    "CSV_FIELDNAMES",
    
    # 實驗入口
    "run_experiment",
]
