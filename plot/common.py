"""
繪圖共用設定
"""

import matplotlib
import matplotlib.pyplot as plt

# 嘗試使用互動後端
try:
    matplotlib.use('TkAgg')
except Exception:
    matplotlib.use('Agg')

# 設置中文字體支持
matplotlib.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False


def setup_figure(figsize=(10, 6)):
    """創建圖表"""
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax


def save_figure(fig, filepath, dpi=300):
    """保存圖表"""
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight')
    print(f"✓ 圖表已保存: {filepath}")


def extract_n_values_from_data(data_dict):
    """從數據字典中提取 N 值列表"""
    n_keys = []
    n_values = []
    for key in sorted(data_dict.keys()):
        if key.startswith('N_'):
            n_val = int(key.split('_')[1])
            n_keys.append(key)
            n_values.append(n_val)
    return n_keys, n_values

