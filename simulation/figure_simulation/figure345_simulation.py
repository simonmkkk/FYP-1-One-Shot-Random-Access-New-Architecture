"""
============================================================================
figure345_simulation - Figure 3, 4, 5 合併模擬
============================================================================

此模組實現 Figure 3, 4, 5 的蒙特卡洛模擬。

同時計算三個性能指標：
- Figure 3: 接入成功率 (P_S)
- Figure 4: 平均接入延遲 (T_a)
- Figure 5: 碰撞概率 (P_C)

這三個 Figure 使用相同的模擬，只是提取不同的指標。
合併執行可避免重複計算，提升效率。

模擬完成後會自動計算 Approximation Error（與近似公式結果對比）。
根據論文定義: Error = |Approximation - Simulation| / |Approximation| * 100%

記憶體優化：每次 N 迴圈後強制 gc，避免記憶體累積。

Input: config 配置, group_paging 模擬引擎, metrics 指標計算
Output: run_figure345_simulation(), load_figure345_simulation_results()
Position: Figure 3, 4, 5 的蒙特卡洛模擬核心

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 標準庫導入
# ============================================================================
import gc  # 垃圾回收模組，用於強制釋放內存
import csv  # CSV 文件讀寫模組
from pathlib import Path  # 物件導向的路徑處理
from datetime import datetime  # 日期時間處理，用於生成時間戳

# ============================================================================
# 本地模組導入
# ============================================================================
from ..core.one_shot_access import simulate_group_paging_multi_samples  # 並行模擬函數
from ..core.metrics import calculate_performance_metrics  # 統計指標計算

# ============================================================================
# 第三方模組導入（解析計算結果）
# ============================================================================
from analytical.figure_analysis import load_figure345_results  # 載入解析計算結果


# ============================================================================
# 路徑常數
# ============================================================================

# 項目根目錄：從當前文件向上三級
# figure345_simulation.py -> figure_simulation/ -> simulation/ -> 專案根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent  # 專案根目錄


# ============================================================================
# 誤差計算函數
# ============================================================================

def calculate_approximation_error(approximation_value: float, simulation_value: float) -> float:
    """
    計算近似誤差百分比（根據論文定義）
    
    論文原文: "The approximation error, which is the absolute difference 
    of the approximation result and the simulation result and normalized 
    by the analytical result"
    
    公式: |Approximation - Simulation| / |Approximation| * 100%
    
    Args:
        approximation_value: 近似公式計算值 (Eqs. 8-10)
        simulation_value: 模擬值
    
    Returns:
        float: 誤差百分比
    """
    # 參數說明（來源 + 是什麼）
    # - approximation_value: float（解析計算的近似值）
    #   來源：load_figure345_results() 載入的解析計算結果
    # - simulation_value: float（蒙特卡洛模擬值）
    #   來源：本模組 run_figure345_simulation() 的模擬結果
    
    if approximation_value != 0:  # 分母非零時正常計算
        return abs(approximation_value - simulation_value) / abs(approximation_value) * 100
    else:  # 分母為零時的特殊處理
        return abs(simulation_value) * 100 if simulation_value != 0 else 0.0


# ============================================================================
# 主模擬函數
# ============================================================================

def run_figure345_simulation(config: dict) -> dict:
    """
    運行 Figure 3, 4, 5 合併模擬
    
    此函數是 Figure 3, 4, 5 模擬的主入口，執行以下步驟：
    1. 從配置中提取模擬參數
    2. 對每個 N 值執行蒙特卡洛模擬
    3. 計算性能指標 (P_S, T_a, P_C)
    4. 計算與解析結果的誤差
    5. 保存結果到 CSV 文件
    
    Args:
        config: 配置字典，包含以下結構：
            - simulation: {M, I_max}
            - scan: {range: {start, stop, step}}
            - performance: {num_samples, num_workers}
            - output: {save_csv: bool}
    
    Returns:
        dict: 結果字典，包含：
            - N_values: N 值列表
            - P_S_values: 接入成功率列表
            - T_a_values: 平均接入延遲列表
            - P_C_values: 碰撞概率列表
            - M, I_max: 模擬參數
            - P_S_error, T_a_error, P_C_error: 誤差列表（可選）
    """
    # 參數說明（來源 + 是什麼）
    # - config: dict（模擬配置字典）
    #   來源：main.py 或 runner 通過 YAML 載入後組裝
    
    # ------------------------------------------------------------------------
    # 步驟 1：提取配置參數
    # ------------------------------------------------------------------------
    M = config['simulation']['M']  # 初始設備數量
    I_max = config['simulation']['I_max']  # 最大 AC 數
    scan_config = config['scan']['range']  # N 值掃描範圍配置
    N_range = range(scan_config['start'], scan_config['stop'], scan_config['step'])  # N 值範圍
    num_samples = config['performance']['num_samples']  # 模擬樣本數
    num_workers = config['performance']['num_workers']  # 並行工作進程數
    
    # ------------------------------------------------------------------------
    # 步驟 2：打印模擬信息
    # ------------------------------------------------------------------------
    print("=" * 70)
    print("Figure 3, 4, 5 合併模擬")
    print("  - Figure 3: Access Success Probability (P_S)")
    print("  - Figure 4: Mean Access Delay (T_a)")
    print("  - Figure 5: Collision Probability (P_C)")
    print("=" * 70)
    print(f"M = {M}, I_max = {I_max}")
    print(f"N 範圍: {scan_config['start']} 到 {scan_config['stop']-1}")
    print(f"樣本數: {num_samples}, 工作進程: {num_workers}")
    print("=" * 70)
    
    # ------------------------------------------------------------------------
    # 步驟 3：初始化結果列表
    # ------------------------------------------------------------------------
    N_values = []  # N 值列表
    P_S_values = []  # 接入成功率列表
    T_a_values = []  # 平均接入延遲列表
    P_C_values = []  # 碰撞概率列表
    
    # ------------------------------------------------------------------------
    # 步驟 4：對每個 N 值執行模擬
    # ------------------------------------------------------------------------
    for N in N_range:  # 遍歷 N 值範圍
        print(f"\n正在模擬 N={N}...")
        
        # 調用並行模擬函數
        results_array = simulate_group_paging_multi_samples(
            M, N, I_max, num_samples, num_workers
        )  # 返回 [num_samples, 3] 的結果矩陣
        
        # 計算統計指標
        means, _ = calculate_performance_metrics(results_array)  # 計算均值和置信區間
        mean_ps, mean_ta, mean_pc = means  # 解包均值
        
        # 保存結果
        N_values.append(N)
        P_S_values.append(mean_ps)
        T_a_values.append(mean_ta)
        P_C_values.append(mean_pc)
        print(f"  結果: P_S={mean_ps:.6f}, T_a={mean_ta:.4f}, P_C={mean_pc:.6f}")
        
        # 記憶體優化：釋放大型結果陣列並強制 gc
        del results_array  # 釋放結果陣列
        gc.collect()  # 強制垃圾回收
    
    # ------------------------------------------------------------------------
    # 步驟 5：組裝結果字典
    # ------------------------------------------------------------------------
    results = {
        'N_values': N_values,
        'P_S_values': P_S_values,
        'T_a_values': T_a_values,
        'P_C_values': P_C_values,
        'M': M,
        'I_max': I_max,
    }
    
    print("\n" + "=" * 70)
    print("Figure 3, 4, 5 合併模擬完成!")
    print("=" * 70)
    
    # ------------------------------------------------------------------------
    # 步驟 6：計算 Approximation Error
    # ------------------------------------------------------------------------
    # 根據論文: Error = |Approximation - Simulation| / |Approximation| * 100%
    print("\n正在計算 Approximation Error...")
    approximation_data = load_figure345_results()  # 載入解析計算結果
    
    if approximation_data is not None:  # 如果有解析結果
        # 建立 N -> index 的映射
        approx_dict = {N: i for i, N in enumerate(approximation_data['N_values'])}
        
        P_S_error = []  # P_S 誤差列表
        T_a_error = []  # T_a 誤差列表
        P_C_error = []  # P_C 誤差列表
        
        for i, N in enumerate(N_values):  # 遍歷模擬結果
            if N in approx_dict:  # 如果有對應的解析結果
                approx_idx = approx_dict[N]
                approx_ps = approximation_data['P_S_values'][approx_idx]
                approx_ta = approximation_data['T_a_values'][approx_idx]
                approx_pc = approximation_data['P_C_values'][approx_idx]
                
                # 計算各指標的誤差
                P_S_error.append(calculate_approximation_error(approx_ps, P_S_values[i]))
                T_a_error.append(calculate_approximation_error(approx_ta, T_a_values[i]))
                P_C_error.append(calculate_approximation_error(approx_pc, P_C_values[i]))
            else:  # 如果找不到對應的 N 值
                P_S_error.append(None)
                T_a_error.append(None)
                P_C_error.append(None)
        
        # 加入誤差數據
        results['P_S_error'] = P_S_error
        results['T_a_error'] = T_a_error
        results['P_C_error'] = P_C_error
        
        print("✓ Approximation Error 計算完成")
    else:  # 沒有解析結果
        print("⚠ 找不到 Approximation 結果，無法計算 Approximation Error")
        print("  請先運行選項 3 進行解析計算")
    
    # ------------------------------------------------------------------------
    # 步驟 7：保存結果到 CSV
    # ------------------------------------------------------------------------
    if config.get('output', {}).get('save_csv', True):  # 檢查是否需要保存
        save_figure345_simulation_results(results)
    
    return results  # 返回結果字典


# ============================================================================
# CSV 保存函數
# ============================================================================

def save_figure345_simulation_results(results: dict):
    """
    保存 Figure 3, 4, 5 合併模擬結果到 CSV 文件
    
    CSV 文件結構：
    - 包含誤差時: N, P_S, T_a, P_C, P_S_error, T_a_error, P_C_error, M, I_max
    - 不含誤差時: N, P_S, T_a, P_C, M, I_max
    
    Args:
        results: 模擬結果字典
    """
    # 參數說明（來源 + 是什麼）
    # - results: dict（模擬結果字典）
    #   來源：run_figure345_simulation() 的返回值
    
    # ------------------------------------------------------------------------
    # 步驟 1：創建結果目錄
    # ------------------------------------------------------------------------
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # 生成時間戳
    result_dir = PROJECT_ROOT / 'result' / 'simulation' / 'figure345' / timestamp  # 結果目錄路徑
    result_dir.mkdir(parents=True, exist_ok=True)  # 創建目錄（含父目錄）
    
    save_path = result_dir / "figure345_simulation.csv"  # CSV 文件路徑
    
    # ------------------------------------------------------------------------
    # 步驟 2：檢查是否有誤差數據
    # ------------------------------------------------------------------------
    has_error = 'P_S_error' in results and results['P_S_error'] is not None
    
    # ------------------------------------------------------------------------
    # 步驟 3：寫入 CSV 文件
    # ------------------------------------------------------------------------
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        
        # 寫入表頭
        if has_error:
            writer.writerow(['N', 'P_S', 'T_a', 'P_C', 'P_S_error', 'T_a_error', 'P_C_error', 'M', 'I_max'])
        else:
            writer.writerow(['N', 'P_S', 'T_a', 'P_C', 'M', 'I_max'])
        
        # 寫入數據
        M = results['M']
        I_max = results['I_max']
        for i in range(len(results['N_values'])):  # 遍歷每個 N 值
            if has_error:
                row = [
                    results['N_values'][i],
                    results['P_S_values'][i],
                    results['T_a_values'][i],
                    results['P_C_values'][i],
                    results['P_S_error'][i] if results['P_S_error'][i] is not None else '',
                    results['T_a_error'][i] if results['T_a_error'][i] is not None else '',
                    results['P_C_error'][i] if results['P_C_error'][i] is not None else '',
                    M,
                    I_max
                ]
            else:
                row = [
                    results['N_values'][i],
                    results['P_S_values'][i],
                    results['T_a_values'][i],
                    results['P_C_values'][i],
                    M,
                    I_max
                ]
            writer.writerow(row)
    
    print(f"✓ 合併模擬結果已保存: {save_path}")


# ============================================================================
# CSV 載入函數
# ============================================================================

def load_figure345_simulation_results() -> dict:
    """
    載入最新的 Figure 3, 4, 5 合併模擬結果
    
    自動尋找最新的時間戳目錄，載入其中的 CSV 結果文件。
    
    Returns:
        dict: 結果字典，包含：
            - N_values, P_S_values, T_a_values, P_C_values
            - M, I_max
            - P_S_error, T_a_error, P_C_error（可選）
        如果找不到結果則返回 None
    """
    # ------------------------------------------------------------------------
    # 步驟 1：檢查結果目錄是否存在
    # ------------------------------------------------------------------------
    result_base = PROJECT_ROOT / 'result' / 'simulation' / 'figure345'
    
    if not result_base.exists():  # 目錄不存在
        return None
    
    # ------------------------------------------------------------------------
    # 步驟 2：找到最新的時間戳目錄
    # ------------------------------------------------------------------------
    timestamp_dirs = sorted(result_base.iterdir(), reverse=True)  # 按時間倒序排列
    if not timestamp_dirs:  # 沒有子目錄
        return None
    
    latest_dir = timestamp_dirs[0]  # 最新目錄
    csv_path = latest_dir / "figure345_simulation.csv"  # CSV 文件路徑
    
    if not csv_path.exists():  # CSV 文件不存在
        return None
    
    # ------------------------------------------------------------------------
    # 步驟 3：讀取 CSV 文件
    # ------------------------------------------------------------------------
    N_values = []
    P_S_values = []
    T_a_values = []
    P_C_values = []
    P_S_error = []
    T_a_error = []
    P_C_error = []
    M = None
    I_max = None
    has_error = False
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:  # 逐行讀取
            N_values.append(int(row['N']))
            P_S_values.append(float(row['P_S']))
            T_a_values.append(float(row['T_a']))
            P_C_values.append(float(row['P_C']))
            
            # 讀取誤差欄位（如果存在）
            if 'P_S_error' in row:
                has_error = True
                P_S_error.append(float(row['P_S_error']) if row['P_S_error'] else None)
                T_a_error.append(float(row['T_a_error']) if row['T_a_error'] else None)
                P_C_error.append(float(row['P_C_error']) if row['P_C_error'] else None)
            
            # 提取 M 和 I_max（只需讀取一次）
            if M is None:
                M = int(row['M'])
                I_max = int(row['I_max'])
    
    # ------------------------------------------------------------------------
    # 步驟 4：組裝結果字典
    # ------------------------------------------------------------------------
    result = {
        'N_values': N_values,
        'P_S_values': P_S_values,
        'T_a_values': T_a_values,
        'P_C_values': P_C_values,
        'M': M,
        'I_max': I_max,
    }
    
    # 加入誤差數據（如果有）
    if has_error:
        result['P_S_error'] = P_S_error
        result['T_a_error'] = T_a_error
        result['P_C_error'] = P_C_error
    
    return result


# ============================================================================
# 模組導出
# ============================================================================

__all__ = [
    "calculate_approximation_error",      # 誤差計算函數
    "run_figure345_simulation",           # 主模擬函數
    "save_figure345_simulation_results",  # CSV 保存函數
    "load_figure345_simulation_results",  # CSV 載入函數
]
