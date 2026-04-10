"""
Figure 3, 4, 5 合併解析數據生成

同時計算:
- Figure 3: 接入成功率 (P_S) vs N
- Figure 4: 平均接入延遲 (T_a) vs N
- Figure 5: 碰撞概率 (P_C) vs N

這三個 Figure 使用相同的理論計算，只是提取不同的指標。
合併執行可避免重複計算，提升效率。

Input: config 配置, theoretical 理論計算模組
Output: run_figure345_analysis(), load_figure345_results()
Position: Figure 3, 4, 5 的解析計算核心

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import csv
from pathlib import Path

from ..theoretical.theoretical import theoretical_calculation
from simulation.core.paths import ANALYTICAL_ROOT


# 項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def run_figure345_analysis(
    config: dict,
    save_csv: bool = True,
    output_dir: Path | None = None,
) -> dict:
    """
    運行 Figure 3, 4, 5 合併解析計算
    
    Args:
        config: 配置字典
        save_csv: 是否保存結果到 CSV
        output_dir: CSV 輸出目錄（None 時使用 result/runs/analytical）
    
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
    print("Figure 3, 4, 5 combined analytical computation")
    print("  - Figure 3: Access Success Probability (P_S)")
    print("  - Figure 4: Mean Access Delay (T_a)")
    print("  - Figure 5: Collision Probability (P_C)")
    print("=" * 70)
    print(f"M = {M}, I_max = {I_max}")
    print(f"N range: {N_start} to {N_stop-1}")
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
    print("Figure 3, 4, 5 combined analytical computation completed!")
    print("=" * 70)
    
    # 保存結果到 CSV
    if save_csv:
        save_figure345_results(results, output_dir=output_dir)
    
    return results


def save_figure345_results(results: dict, output_dir: Path | None = None):
    """保存 Figure 3, 4, 5 合併解析結果到 CSV 文件"""
    # 統一輸出到 result/runs/analytical，避免重複目錄
    result_dir = Path(output_dir) if output_dir is not None else ANALYTICAL_ROOT
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
    
    print(f"✓ Combined analytical results saved: {save_path}")


def load_figure345_results() -> dict:
    """
    從最新的 CSV 文件讀取 Figure 3, 4, 5 合併解析結果
    
    Returns:
        結果字典，如果找不到則返回 None
    """
    csv_path = ANALYTICAL_ROOT / "figure345_analytical.csv"
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
