"""
Figure 2 解析數據生成

近似誤差分析 - 按照論文 Figure 2
誤差 = |Analytical - Approximation| / |Analytical| * 100%
"""

import csv
from pathlib import Path
from datetime import datetime
from .figure1_analysis import run_figure1_analysis

# 項目根目錄
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def run_figure2_analysis(config: dict, save_csv: bool = True) -> dict:
    """
    運行 Figure 2 解析計算（基於 Figure 1 數據）
    
    Args:
        config: 配置字典
        save_csv: 是否保存結果到 CSV
    
    Returns:
        結果字典
    """
    n_values = config['n_values']
    
    print("=" * 60)
    print("Figure 2: Approximation Error Analysis")
    print(f"N 值: {n_values}")
    print("=" * 60)
    
    # 先運行 Figure 1 獲取基礎數據（不保存 CSV，因為 Figure 2 會自己保存）
    fig1_data = run_figure1_analysis(config, save_csv=False)
    
    print("\n正在計算誤差數據...")
    
    error_results = {}
    
    for key, data in fig1_data.items():
        N_S_error = []
        N_C_error = []
        
        for i in range(len(data['analytical_N_S'])):
            anal_ns = data['analytical_N_S'][i]
            approx_ns = data['approx_N_S'][i]
            # 計算相對誤差: |analytical - approx| / |analytical| * 100%
            if anal_ns != 0:
                error_ns = abs(anal_ns - approx_ns) / abs(anal_ns) * 100
            else:
                # 當 analytical = 0 時，直接用 approx 值作為誤差
                error_ns = abs(approx_ns)
            N_S_error.append(error_ns)
            
            anal_nc = data['analytical_N_C'][i]
            approx_nc = data['approx_N_C'][i]
            # 計算相對誤差
            if anal_nc != 0:
                error_nc = abs(anal_nc - approx_nc) / abs(anal_nc) * 100
            else:
                # 當 analytical = 0 時，直接用 approx 值作為誤差
                error_nc = abs(approx_nc)
            N_C_error.append(error_nc)
        
        error_results[key] = {
            'M_values': data['M_values'],
            'M_over_N': data['M_over_N'],
            'N_S_error': N_S_error,
            'N_C_error': N_C_error,
            # 保留原始數據供繪圖使用
            'analytical_N_S': data['analytical_N_S'],
            'analytical_N_C': data['analytical_N_C'],
            'approx_N_S': data['approx_N_S'],
            'approx_N_C': data['approx_N_C'],
        }
    
    print("\n" + "=" * 60)
    print("Figure 2 解析計算完成!")
    print("=" * 60)
    
    # 保存結果到 CSV
    if save_csv:
        save_figure2_results(error_results)
    
    return error_results


def save_figure2_results(results: dict):
    """保存 Figure 2 解析結果到 CSV 文件"""
    # 創建結果目錄
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / 'analytical' / 'figure2' / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    
    # 為每個 N 值保存一個 CSV 文件
    for key, data in results.items():
        if key.startswith('N_'):
            N_value = key.split('_')[1]
            save_path = result_dir / f"figure2_N{N_value}.csv"
            
            with open(save_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # 寫入表頭
                writer.writerow(['M', 'M/N', 'analytical_N_S', 'analytical_N_C', 
                                'approx_N_S', 'approx_N_C', 'N_S_error(%)', 'N_C_error(%)'])
                # 寫入數據
                for i in range(len(data['M_values'])):
                    writer.writerow([
                        data['M_values'][i],
                        data['M_over_N'][i],
                        data['analytical_N_S'][i],
                        data['analytical_N_C'][i],
                        data['approx_N_S'][i],
                        data['approx_N_C'][i],
                        data['N_S_error'][i],
                        data['N_C_error'][i]
                    ])
            
            print(f"✓ 解析結果已保存: {save_path}")


def load_figure2_results() -> dict:
    """從最新的 CSV 文件讀取 Figure 2 解析結果"""
    result_base = PROJECT_ROOT / 'result' / 'analytical' / 'figure2'
    
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
    for csv_file in latest_dir.glob('figure2_N*.csv'):
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
                'N_S_error': [],
                'N_C_error': [],
            }
            for row in reader:
                data['M_values'].append(int(row['M']))
                data['M_over_N'].append(float(row['M/N']))
                data['analytical_N_S'].append(float(row['analytical_N_S']))
                data['analytical_N_C'].append(float(row['analytical_N_C']))
                data['approx_N_S'].append(float(row['approx_N_S']))
                data['approx_N_C'].append(float(row['approx_N_C']))
                data['N_S_error'].append(float(row['N_S_error(%)']))
                data['N_C_error'].append(float(row['N_C_error(%)']))
            
            results[key] = data
            print(f"  ✓ 讀取 N={N_value}: {len(data['M_values'])} 個數據點")
    
    return results if results else None

