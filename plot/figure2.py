"""
Figure 2 繪製

Approximation Error - 按照論文 Figure 2 樣式
誤差 = |Analytical - Approximation| / |Analytical| * 100%

佈局：上面兩個 N 值的子圖，下面一個合併圖
線條樣式規則（與 Figure 1 對應）：
- 第一個 N 值: 實線+圓圈 (N_S) / 點線+圓圈 (N_C)
- 第二個 N 值: 實線無標記 (N_S) / 虛線無標記 (N_C)

Input: Figure 2 數據 (誤差數據)
Output: plot_figure2() 繪圖函數
Position: Figure 2 可視化

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.gridspec import GridSpec
from .common import extract_n_values_from_data


def plot_figure2(data: dict, save_path: str = None, show: bool = False):
    """
    繪製 Figure 2 - 按照論文樣式
    
    子圖結構（2行佈局）：
    - 上排: (a) 第一個 N 值, (b) 第二個 N 值
    - 下排: (c) All Combined (在中間)
    
    Args:
        data: 誤差數據字典
        save_path: 保存路徑
        show: 是否顯示圖表
    
    Returns:
        Figure 對象
    """
    available_N_keys, available_N_values = extract_n_values_from_data(data)
    
    if not available_N_keys:
        raise ValueError("數據中沒有找到任何 N 值")
    
    num_N_values = len(available_N_keys)
    
    # 創建 2 行佈局
    fig = plt.figure(figsize=(6 * num_N_values, 10))
    gs = GridSpec(2, num_N_values, figure=fig, height_ratios=[1, 1], hspace=0.3, wspace=0.3)
    
    # 上排的子圖
    top_axes = [fig.add_subplot(gs[0, i]) for i in range(num_N_values)]
    # 下排的合併圖（放在中間位置）
    center_idx = num_N_values // 2
    ax_combined = fig.add_subplot(gs[1, center_idx])
    
    # ==================== 繪製每個 N 值的誤差圖 (上排) ====================
    for idx, (N_key, N_value) in enumerate(zip(available_N_keys, available_N_values)):
        ax = top_axes[idx]
        N_data = data[N_key]
        M_over_N = np.array(N_data['M_over_N'])
        N_S_error = np.array(N_data['N_S_error'])
        N_C_error = np.array(N_data['N_C_error'])
        
        # 過濾掉 M/N=0 的數據點（避免異常值）
        valid_mask = M_over_N > 0
        M_over_N = M_over_N[valid_mask]
        N_S_error = N_S_error[valid_mask]
        N_C_error = N_C_error[valid_mask]
        
        # 根據論文樣式選擇線條類型
        if idx == 0:
            # 第一個 N: 實線+圓圈 / 點線+圓圈
            marker_every = max(1, len(M_over_N) // 15)
            ax.plot(M_over_N, N_S_error, 'k-', linewidth=1.5,
                    marker='o', markersize=5, markevery=marker_every,
                    markerfacecolor='none', markeredgecolor='black', markeredgewidth=1.2,
                    label=rf'N={N_value} $N_{{S,1}}$/N')
            ax.plot(M_over_N, N_C_error, 'k:', linewidth=1.5,
                    marker='o', markersize=5, markevery=marker_every,
                    markerfacecolor='none', markeredgecolor='black', markeredgewidth=1.2,
                    label=rf'N={N_value} $N_{{C,1}}$/N')
        else:
            # 第二個 N: 實線無標記 / 虛線無標記
            ax.plot(M_over_N, N_S_error, 'k-', linewidth=1.5,
                    label=rf'N={N_value} $N_{{S,1}}$/N')
            ax.plot(M_over_N, N_C_error, 'k--', linewidth=1.5,
                    label=rf'N={N_value} $N_{{C,1}}$/N')
        
        _setup_axis(ax)
        subplot_label = chr(ord('a') + idx)
        ax.set_title(f'({subplot_label}) N={N_value} Approximation Error', fontsize=11, pad=10)
        ax.legend(loc='best', fontsize=8, framealpha=0.9)
    
    # ==================== 合併圖 (下排) ====================
    for idx, (N_key, N_value) in enumerate(zip(available_N_keys, available_N_values)):
        N_data = data[N_key]
        M_over_N = np.array(N_data['M_over_N'])
        N_S_error = np.array(N_data['N_S_error'])
        N_C_error = np.array(N_data['N_C_error'])
        
        # 過濾掉 M/N=0 的數據點（避免異常值）
        valid_mask = M_over_N > 0
        M_over_N = M_over_N[valid_mask]
        N_S_error = N_S_error[valid_mask]
        N_C_error = N_C_error[valid_mask]
        
        if idx == 0:
            marker_every = max(1, len(M_over_N) // 15)
            ax_combined.plot(M_over_N, N_S_error, 'k-', linewidth=1.5,
                    marker='o', markersize=4, markevery=marker_every,
                    markerfacecolor='none', markeredgecolor='black', markeredgewidth=1,
                    label=rf'N={N_value} $N_{{S,1}}$/N')
            ax_combined.plot(M_over_N, N_C_error, 'k:', linewidth=1.5,
                    marker='o', markersize=4, markevery=marker_every,
                    markerfacecolor='none', markeredgecolor='black', markeredgewidth=1,
                    label=rf'N={N_value} $N_{{C,1}}$/N')
        else:
            ax_combined.plot(M_over_N, N_S_error, 'k-', linewidth=1.5,
                    label=rf'N={N_value} $N_{{S,1}}$/N')
            ax_combined.plot(M_over_N, N_C_error, 'k--', linewidth=1.5,
                    label=rf'N={N_value} $N_{{C,1}}$/N')
    
    # 添加曲線標註 (帶箭頭) - 只在合併圖中添加
    ax_combined.annotate(r'$N_{S,1}$/N', xy=(8, 200), xytext=(9, 10),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'),
                fontsize=12, ha='center')
    
    ax_combined.annotate(r'$N_{C,1}$/N', xy=(6, 1), xytext=(6.5, 2),
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'),
                fontsize=12, ha='center')
    
    _setup_axis(ax_combined)
    subplot_label = chr(ord('a') + num_N_values)
    ax_combined.set_title(f'({subplot_label}) All Combined', fontsize=11, pad=10)
    ax_combined.legend(loc='best', fontsize=8, framealpha=0.9)
    
    # 添加總標題
    n_values_str = ', '.join([str(n) for n in available_N_values])
    fig.suptitle(rf'Fig. 2.   Approximation error of $N_{{S,1}}/N$ and $N_{{C,1}}/N$ (N={{{n_values_str}}})',
                 fontsize=12, y=0.02)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.08, top=0.95)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Figure 2 已保存: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def _setup_axis(ax):
    """設置共用的軸樣式"""
    ax.set_xlabel('M/N', fontsize=11)
    ax.set_ylabel('Approximation Error (%)', fontsize=11)
    ax.set_xlim(0, 10)
    ax.set_xticks(np.arange(0, 12, 2))  # 論文: 0, 2, 4, 6, 8, 10
    ax.set_yscale('log')
    ax.set_ylim(1e-2, 1e3)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

