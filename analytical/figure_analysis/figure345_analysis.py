"""
Figure 3, 4, 5 合併解析數據生成

同時計算:
- Figure 3: 接入成功率 (P_S) vs N
- Figure 4: 平均接入延遲 (T_a) vs N
- Figure 5: 碰撞概率 (P_C) vs N

這三個 Figure 使用相同的理論計算，只是提取不同的指標。
合併執行可避免重複計算，提升效率。
"""

import csv
from pathlib import Path
from datetime import datetime

from ..theoretical import theoretical_calculation

# 項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def run_figure345_analysis(config: dict, save_csv: bool = True) -> dict:
    """
    運行 Figure 3, 4, 5 合併解析計算
    
    Args:
        config: 配置字典
        save_csv: 是否保存結果到 CSV
    
    Returns:
        結果字典，包含 P_S, T_a, P_C 三個指標
    """
    M = config['M']
    I_max = config['I_max']
    N_start = config['N_start']
    N_stop = config['N_stop']
    N_step = config['N_step']
    N_range = range(N_start, N_stop, N_step)
    
    print("=" * 70)
    print("Figure 3, 4, 5 合併解析計算")
    print("  - Figure 3: Access Success Probability (P_S)")
    print("  - Figure 4: Mean Access Delay (T_a)")
    print("  - Figure 5: Collision Probability (P_C)")
    print("=" * 70)
    print(f"M = {M}, I_max = {I_max}")
    print(f"N 範圍: {N_start} 到 {N_stop-1}")
    print("=" * 70)
    
    N_values = []
    P_S_values = []
    T_a_values = []
    P_C_values = []
    
    for N in N_range:
        P_S, T_a, P_C, N_s, K = theoretical_calculation(M, N, I_max)
        N_values.append(N)
        P_S_values.append(P_S)
        T_a_values.append(T_a)
        P_C_values.append(P_C)
        print(f"  N={N}: P_S={P_S:.6f}, T_a={T_a:.4f}, P_C={P_C:.6f}")
    
    results = {
        'N_values': N_values,
        'P_S_values': P_S_values,
        'T_a_values': T_a_values,
        'P_C_values': P_C_values,
        'M': M,
        'I_max': I_max,
    }
    
    print("\n" + "=" * 70)
    print("Figure 3, 4, 5 合併解析計算完成!")
    print("=" * 70)
    
    # 保存結果到 CSV
    if save_csv:
        save_figure345_results(results)
    
    return results


def save_figure345_results(results: dict):
    """保存 Figure 3, 4, 5 合併解析結果到 CSV 文件"""
    # 創建結果目錄
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / 'analytical' / 'figure345' / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    
    save_path = result_dir / "figure345_analytical.csv"
    
    with open(save_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # 寫入表頭
        writer.writerow(['N', 'P_S', 'T_a', 'P_C', 'M', 'I_max'])
        # 寫入數據
        M = results['M']
        I_max = results['I_max']
        for i in range(len(results['N_values'])):
            writer.writerow([
                results['N_values'][i],
                results['P_S_values'][i],
                results['T_a_values'][i],
                results['P_C_values'][i],
                M,
                I_max
            ])
    
    print(f"✓ 合併解析結果已保存: {save_path}")


def load_figure345_results() -> dict:
    """
    從最新的 CSV 文件讀取 Figure 3, 4, 5 合併解析結果
    
    Returns:
        結果字典，如果找不到則返回 None
    """
    result_base = PROJECT_ROOT / 'result' / 'analytical' / 'figure345'
    
    if not result_base.exists():
        return None
    
    # 找到最新的時間戳目錄
    timestamp_dirs = sorted(result_base.iterdir(), reverse=True)
    if not timestamp_dirs:
        return None
    
    latest_dir = timestamp_dirs[0]
    csv_path = latest_dir / "figure345_analytical.csv"
    
    if not csv_path.exists():
        return None
    
    # 讀取 CSV
    N_values = []
    P_S_values = []
    T_a_values = []
    P_C_values = []
    M = None
    I_max = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            N_values.append(int(row['N']))
            P_S_values.append(float(row['P_S']))
            T_a_values.append(float(row['T_a']))
            P_C_values.append(float(row['P_C']))
            if M is None:
                M = int(row['M'])
                I_max = int(row['I_max'])
    
    return {
        'N_values': N_values,
        'P_S_values': P_S_values,
        'T_a_values': T_a_values,
        'P_C_values': P_C_values,
        'M': M,
        'I_max': I_max,
    }
