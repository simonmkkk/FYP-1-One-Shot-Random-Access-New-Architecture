"""
Figure 3, 4, 5 合併模擬

同時計算:
- Figure 3: 接入成功率 (P_S)
- Figure 4: 平均接入延遲 (T_a)
- Figure 5: 碰撞概率 (P_C)

這三個 Figure 使用相同的模擬，只是提取不同的指標。
合併執行可避免重複計算，提升效率。

模擬完成後會自動計算 Approximation Error（與 Analytical 結果對比）。

記憶體優化：每次 N 迴圈後強制 gc，避免記憶體累積。
"""

import gc
import csv
from pathlib import Path
from datetime import datetime

from ..core.group_paging import simulate_group_paging_multi_samples, clear_thread_local_rng
from ..core.metrics import calculate_performance_metrics
from analytical.figure_analysis import load_figure345_results

# 項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def calculate_approximation_error(analytical_value: float, simulation_value: float) -> float:
    """
    計算近似誤差百分比
    
    公式: |Analytical - Simulation| / |Analytical| * 100%
    
    Args:
        analytical_value: 解析計算值
        simulation_value: 模擬值
    
    Returns:
        誤差百分比
    """
    if analytical_value != 0:
        return abs(analytical_value - simulation_value) / abs(analytical_value) * 100
    else:
        return abs(simulation_value) * 100 if simulation_value != 0 else 0.0


def run_figure345_simulation(config: dict) -> dict:
    """
    運行 Figure 3, 4, 5 合併模擬
    
    Args:
        config: 配置字典
    
    Returns:
        結果字典，包含 P_S, T_a, P_C 三個指標
    """
    M = config['simulation']['M']
    I_max = config['simulation']['I_max']
    scan_config = config['scan']['range']
    N_range = range(scan_config['start'], scan_config['stop'], scan_config['step'])
    num_samples = config['performance']['num_samples']
    num_workers = config['performance']['num_workers']
    
    print("=" * 70)
    print("Figure 3, 4, 5 合併模擬")
    print("  - Figure 3: Access Success Probability (P_S)")
    print("  - Figure 4: Mean Access Delay (T_a)")
    print("  - Figure 5: Collision Probability (P_C)")
    print("=" * 70)
    print(f"M = {M}, I_max = {I_max}")
    print(f"N 範圍: {scan_config['start']} 到 {scan_config['stop']-1}")
    print(f"樣本數: {num_samples}, 工作線程: {num_workers}")
    print("=" * 70)
    
    N_values = []
    P_S_values = []
    T_a_values = []
    P_C_values = []
    
    for N in N_range:
        print(f"\n正在模擬 N={N}...")
        
        results_array = simulate_group_paging_multi_samples(
            M, N, I_max, num_samples, num_workers
        )
        means, _ = calculate_performance_metrics(results_array)
        mean_ps, mean_ta, mean_pc = means
        
        N_values.append(N)
        P_S_values.append(mean_ps)
        T_a_values.append(mean_ta)
        P_C_values.append(mean_pc)
        print(f"  結果: P_S={mean_ps:.6f}, T_a={mean_ta:.4f}, P_C={mean_pc:.6f}")
        
        # 記憶體優化：釋放大型結果陣列並強制 gc
        del results_array
        gc.collect()
    
    # 清理 thread-local RNG，釋放線程記憶體
    clear_thread_local_rng()
    gc.collect()
    
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
    
    # 計算 Approximation Error（與 Analytical 結果對比）
    print("\n正在計算 Approximation Error...")
    analytical_data = load_figure345_results()
    
    if analytical_data is not None:
        # 建立 N -> index 的映射
        anal_dict = {N: i for i, N in enumerate(analytical_data['N_values'])}
        
        P_S_error = []
        T_a_error = []
        P_C_error = []
        
        for i, N in enumerate(N_values):
            if N in anal_dict:
                anal_idx = anal_dict[N]
                anal_ps = analytical_data['P_S_values'][anal_idx]
                anal_ta = analytical_data['T_a_values'][anal_idx]
                anal_pc = analytical_data['P_C_values'][anal_idx]
                
                P_S_error.append(calculate_approximation_error(anal_ps, P_S_values[i]))
                T_a_error.append(calculate_approximation_error(anal_ta, T_a_values[i]))
                P_C_error.append(calculate_approximation_error(anal_pc, P_C_values[i]))
            else:
                # 如果找不到對應的 N 值，設為 None
                P_S_error.append(None)
                T_a_error.append(None)
                P_C_error.append(None)
        
        results['P_S_error'] = P_S_error
        results['T_a_error'] = T_a_error
        results['P_C_error'] = P_C_error
        
        print("✓ Approximation Error 計算完成")
    else:
        print("⚠ 找不到 Analytical 結果，無法計算 Approximation Error")
        print("  請先運行選項 3 進行解析計算")
    
    # 保存結果到 CSV
    if config.get('output', {}).get('save_csv', True):
        save_figure345_simulation_results(results)
    
    return results


def save_figure345_simulation_results(results: dict):
    """保存 Figure 3, 4, 5 合併模擬結果到 CSV 文件（包含 Approximation Error）"""
    # 創建結果目錄
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / 'simulation' / 'figure345' / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = result_dir / "figure345_simulation.csv"
    
    # 檢查是否有誤差數據
    has_error = 'P_S_error' in results and results['P_S_error'] is not None
    
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
        for i in range(len(results['N_values'])):
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


def load_figure345_simulation_results() -> dict:
    """
    載入最新的 Figure 3, 4, 5 合併模擬結果（包含 Approximation Error）
    
    Returns:
        結果字典，如果找不到則返回 None
    """
    result_base = PROJECT_ROOT / 'result' / 'simulation' / 'figure345'
    
    if not result_base.exists():
        return None
    
    # 找到最新的時間戳目錄
    timestamp_dirs = sorted(result_base.iterdir(), reverse=True)
    if not timestamp_dirs:
        return None
    
    latest_dir = timestamp_dirs[0]
    csv_path = latest_dir / "figure345_simulation.csv"
    
    if not csv_path.exists():
        return None
    
    # 讀取 CSV
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
        for row in reader:
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
            
            if M is None:
                M = int(row['M'])
                I_max = int(row['I_max'])
    
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
