"""
Figure 1 解析數據生成

NS,1/N & NC,1/N vs M/N - 分析模型 vs 近似公式

Input: config 配置, formulas 公式模組
Output: run_figure1_analysis(), load_figure1_results()
Position: Figure 1 的解析計算核心

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import csv
import os
import time
from pathlib import Path
from datetime import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed
from ..formulas.formulas import (
    paper_formula_2_collision_raos_exact,
    paper_formula_3_success_raos_exact,
    paper_formula_4_success_approx,
    paper_formula_5_collision_approx,
)
# 可選的計時器支持
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from performance import SimpleTimer


def _get_actual_n_jobs(n_jobs: int) -> int:
    """獲取實際使用的 CPU 核心數"""
    if n_jobs == -1:
        return os.cpu_count() or 1
    return n_jobs


def _parallel_compute(func, args_list, n_jobs: int, desc: str = "計算中"):
    """
    並行計算輔助函數
    
    使用 ProcessPoolExecutor 實現多進程並行計算，可充分利用多核 CPU。
    
    Args:
        func: 計算函數（必須是頂層函數，可被 pickle）
        args_list: 參數列表，每個元素是傳給 func 的參數元組
        n_jobs: 並行數 (-1 表示使用所有 CPU 核心)
        desc: 描述
    
    Returns:
        結果列表（保持輸入順序）
    """
    actual_n_jobs = _get_actual_n_jobs(n_jobs)
    total_tasks = len(args_list)
    print(f"  {desc}... (使用 {actual_n_jobs} 個進程, 共 {total_tasks} 個任務)")
    
    start_time = time.time()
    
    # 使用 ProcessPoolExecutor 進行多進程並行
    results = [None] * total_tasks
    completed = 0
    
    with ProcessPoolExecutor(max_workers=actual_n_jobs) as executor:
        # 提交所有任務，保存 future 到索引的映射
        future_to_idx = {
            executor.submit(func, *args): idx 
            for idx, args in enumerate(args_list)
        }
        
        # 收集結果
        for future in as_completed(future_to_idx):
            idx = future_to_idx[future]
            results[idx] = future.result()
            completed += 1
            
            # 進度顯示（每 10% 或最後一個顯示一次）
            if completed % max(1, total_tasks // 10) == 0 or completed == total_tasks:
                progress = completed / total_tasks * 100
                print(f"    進度: {completed}/{total_tasks} ({progress:.0f}%)")
    
    elapsed = time.time() - start_time
    print(f"  完成! 耗時: {elapsed:.2f}秒")
    
    return results

# 項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def compute_single_point(M, N):
    """計算單個(M,N)點的分析模型和近似公式結果"""
    start_time = time.time()
    
    # 處理 M=0 的邊界情況
    if M == 0:
        N_S_anal = 0
        N_C_anal = 0
        N_S_approx = 0
        N_C_approx = 0
    else:
        N_S_anal = paper_formula_3_success_raos_exact(M, N)
        N_C_anal = paper_formula_2_collision_raos_exact(M, N)
        N_S_approx = paper_formula_4_success_approx(M, N)
        N_C_approx = paper_formula_5_collision_approx(M, N)
    
    elapsed = time.time() - start_time
    
    return (M, N_S_anal/N if N > 0 else 0, N_C_anal/N if N > 0 else 0, 
            N_S_approx/N if N > 0 else 0, N_C_approx/N if N > 0 else 0, elapsed)


def run_figure1_analysis(config: dict, save_csv: bool = True, timer: 'SimpleTimer' = None) -> dict:
    """
    運行 Figure 1 解析計算
    
    Args:
        config: 配置字典
        save_csv: 是否保存結果到 CSV
        timer: 可選的計時器（用於記錄各 N 值的計算時間）
    
    Returns:
        結果字典
    """
    n_values = config['n_values']
    m_over_n_max = config['m_over_n_max']
    m_start = config['m_start']
    n_jobs = config.get('n_jobs', -1)
    
    actual_n_jobs = _get_actual_n_jobs(n_jobs)
    
    print("=" * 60)
    print("Figure 1: Analytical Model vs Approximation")
    print(f"N 值: {n_values}")
    print(f"M 範圍: {m_start} 到 {m_over_n_max}*N")
    print(f"CPU 核心: {actual_n_jobs}")
    print("=" * 60)
    
    results = {}
    
    for N in n_values:
        print(f"\n正在計算 N={N} 的數據...")
        
        # 論文: integer valued of M ranging from 1 to 10N
        M_range = list(range(m_start, m_over_n_max * N + 1))
        print(f"  M 範圍: {m_start} 到 {m_over_n_max * N}，共 {len(M_range)} 個數據點")
        
        # 記錄每個 N 的計算時間
        n_start_time = time.time()
        
        args_list = [(M, N) for M in M_range]
        results_list = _parallel_compute(
            compute_single_point, args_list, n_jobs, 
            f"計算 N={N}"
        )
        
        # 記錄到計時器
        n_elapsed = time.time() - n_start_time
        if timer:
            timer.record(f"N={N} 計算", n_elapsed)
        
        M_values = [r[0] for r in results_list]
        analytical_N_S = [r[1] for r in results_list]
        analytical_N_C = [r[2] for r in results_list]
        approx_N_S = [r[3] for r in results_list]
        approx_N_C = [r[4] for r in results_list]
        
        results[f'N_{N}'] = {
            'M_values': M_values,
            'M_over_N': [m/N for m in M_values],
            'analytical_N_S': analytical_N_S,
            'analytical_N_C': analytical_N_C,
            'approx_N_S': approx_N_S,
            'approx_N_C': approx_N_C
        }
    
    print("\n" + "=" * 60)
    print("Figure 1 解析計算完成!")
    print("=" * 60)
    
    # 保存結果到 CSV
    if save_csv:
        save_figure1_results(results)
    
    return results


def save_figure1_results(results: dict):
    """保存 Figure 1 解析結果到 CSV 文件"""
    # 創建結果目錄
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / 'analytical' / 'figure1' / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # 為每個 N 值保存一個 CSV 文件
    for key, data in results.items():
        if key.startswith('N_'):
            N_value = key.split('_')[1]
            save_path = result_dir / f"figure1_N{N_value}.csv"
            
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 寫入表頭
                writer.writerow(['M', 'M/N', 'analytical_N_S', 'analytical_N_C', 'approx_N_S', 'approx_N_C'])
                # 寫入數據
                for i in range(len(data['M_values'])):
                    writer.writerow([
                        data['M_values'][i],
                        data['M_over_N'][i],
                        data['analytical_N_S'][i],
                        data['analytical_N_C'][i],
                        data['approx_N_S'][i],
                        data['approx_N_C'][i]
                    ])
            
            print(f"✓ 解析結果已保存: {save_path}")


def load_figure1_results() -> dict:
    """從最新的 CSV 文件讀取 Figure 1 解析結果"""
    result_base = PROJECT_ROOT / 'result' / 'analytical' / 'figure1'
    
    if not result_base.exists():
        return None
    
    # 找到最新的時間戳目錄
    timestamp_dirs = sorted(result_base.iterdir(), reverse=True)
    if not timestamp_dirs:
        return None
    
    latest_dir = timestamp_dirs[0]
    print(f"✓ 讀取最新數據: {latest_dir}")
    
    results = {}
    
    # 讀取所有 CSV 文件
    for csv_file in latest_dir.glob('figure1_N*.csv'):
        N_value = csv_file.stem.split('_N')[1]
        key = f'N_{N_value}'
        
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = {
                'M_values': [],
                'M_over_N': [],
                'analytical_N_S': [],
                'analytical_N_C': [],
                'approx_N_S': [],
                'approx_N_C': [],
            }
            for row in reader:
                data['M_values'].append(int(row['M']))
                data['M_over_N'].append(float(row['M/N']))
                data['analytical_N_S'].append(float(row['analytical_N_S']))
                data['analytical_N_C'].append(float(row['analytical_N_C']))
                data['approx_N_S'].append(float(row['approx_N_S']))
                data['approx_N_C'].append(float(row['approx_N_C']))
            
            results[key] = data
            print(f"  ✓ 讀取 N={N_value}: {len(data['M_values'])} 個數據點")
    
    return results if results else None

