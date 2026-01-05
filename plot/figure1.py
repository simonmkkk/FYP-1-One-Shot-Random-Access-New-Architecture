"""
Figure 1 繪製

NS,1/N & NC,1/N vs M/N
按照論文 Figure 1 樣式實現

線條樣式規則（按照論文）：
- 第一個 N 值: 實線+圓圈 (N_S) / 點線+圓圈 (N_C)
- 第二個 N 值: 實線無標記 (N_S) / 虛線無標記 (N_C)  
- Approximation: 細點線 (N_S, Eq.4) / 點劃線 (N_C, Eq.5)

佈局：上面三個子圖，下面一個合併圖

Input: Figure 1 數據 (analytical 或 simulation)
Output: plot_figure1() 繪圖函數
Position: Figure 1 可視化

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import matplotlib.pyplot as plt
import numpy as np
from .common import extract_n_values_from_data


def plot_figure1(data: dict, data_type: str = 'analytical', save_path: str = None, show: bool = False):
    """
    繪製 Figure 1 - 按照論文樣式
    
    子圖結構（2行佈局）：
    - 上排: (a) 第一個 N 值, (b) 第二個 N 值, (c) Approximation
    - 下排: (d) All Combined (橫跨整行)
    
    Args:
        data: 數據字典
        data_type: 'analytical' 或 'simulation'
        save_path: 保存路徑
        show: 是否顯示圖表
    
    Returns:
        Figure 對象
    """
    available_N_keys, available_N_values = extract_n_values_from_data(data)
    
    if not available_N_keys:
        raise ValueError("數據中沒有找到任何 N 值")
    
    num_N_values = len(available_N_keys)
    # 上排子圖數 = N 值數量 + 1 (Approximation)
    num_top_subplots = num_N_values + 1
    
    # 創建 2 行佈局：上面 num_top_subplots 個，下面 1 個在中間
    fig = plt.figure(figsize=(6 * num_top_subplots, 10))
    
    # 使用 GridSpec 來創建佈局
    from matplotlib.gridspec import GridSpec
    gs = GridSpec(2, num_top_subplots, figure=fig, height_ratios=[1, 1], hspace=0.3, wspace=0.3)
    
    # 上排的子圖
    top_axes = [fig.add_subplot(gs[0, i]) for i in range(num_top_subplots)]
    # 下排的合併圖（放在中間位置，與 (b) 對齊）
    center_idx = num_top_subplots // 2
    ax_combined = fig.add_subplot(gs[1, center_idx])
    
    # ==================== 繪製每個 N 值的 Analytical 結果 (上排) ====================
    for idx, (N_key, N_value) in enumerate(zip(available_N_keys, available_N_values)):
        ax = top_axes[idx]
        
        if data_type == 'analytical':
            N_data = data[N_key]
            M_over_N = np.array(N_data['M_over_N'])
            analytical_N_S = np.array(N_data['analytical_N_S'])
            analytical_N_C = np.array(N_data['analytical_N_C'])
            
            # 根據論文樣式選擇線條類型
            if idx == 0:
                # 第一個 N: 實線+圓圈 / 點線+圓圈
                marker_every = max(1, len(M_over_N) // 15)
                ax.plot(M_over_N, analytical_N_S, 'k-', linewidth=1.5, 
                        marker='o', markersize=5, markevery=marker_every,
                        markerfacecolor='none', markeredgecolor='black', markeredgewidth=1.2,
                        label=rf'N={N_value} $N_{{S,1}}$/N Analytical Model')
                ax.plot(M_over_N, analytical_N_C, 'k:', linewidth=1.5,
                        marker='o', markersize=5, markevery=marker_every,
                        markerfacecolor='none', markeredgecolor='black', markeredgewidth=1.2,
                        label=rf'N={N_value} $N_{{C,1}}$/N Analytical Model')
            else:
                # 第二個 N: 實線無標記 / 虛線無標記
                ax.plot(M_over_N, analytical_N_S, 'k-', linewidth=1.5,
                        label=rf'N={N_value} $N_{{S,1}}$/N Analytical Model')
                ax.plot(M_over_N, analytical_N_C, 'k--', linewidth=1.5,
                        label=rf'N={N_value} $N_{{C,1}}$/N Analytical Model')
            
            _setup_axis(ax)
            subplot_label = chr(ord('a') + idx)
            ax.set_title(f'({subplot_label}) N={N_value} Analytical', fontsize=11, pad=10)
            ax.legend(loc='center', bbox_to_anchor=(0.5, 0.55), fontsize=7, framealpha=0.9)
    
    # ==================== Approximation 子圖 (上排) ====================
    ax_approx = top_axes[num_N_values]
    
    if data_type == 'analytical' and available_N_keys:
        N_key = available_N_keys[0]
        N_data = data[N_key]
        M_over_N = np.array(N_data['M_over_N'])
        approx_N_S = np.array(N_data['approx_N_S'])
        approx_N_C = np.array(N_data['approx_N_C'])
        
        # Approximation: 細點線 (N_S) / 點劃線 (N_C)
        ax_approx.plot(M_over_N, approx_N_S, color='black', linestyle=':', linewidth=1.5,
                label=r'$N_{S,1}$/N Derived Performance Metric, Eq. (4)')
        ax_approx.plot(M_over_N, approx_N_C, color='black', linestyle='-.', linewidth=1.5,
                label=r'$N_{C,1}$/N Derived Performance Metric, Eq. (5)')
        
        _setup_axis(ax_approx)
        subplot_label = chr(ord('a') + num_N_values)
        ax_approx.set_title(f'({subplot_label}) Approximation', fontsize=11, pad=10)
        ax_approx.legend(loc='center', bbox_to_anchor=(0.5, 0.55), fontsize=7, framealpha=0.9)
    
    # ==================== 全部合一子圖 (下排) ====================
    if data_type == 'analytical' and available_N_keys:
        # 繪製所有 N 值的 Analytical 結果
        for idx, (N_key, N_value) in enumerate(zip(available_N_keys, available_N_values)):
            N_data = data[N_key]
            M_over_N = np.array(N_data['M_over_N'])
            analytical_N_S = np.array(N_data['analytical_N_S'])
            analytical_N_C = np.array(N_data['analytical_N_C'])
            
            if idx == 0:
                # 第一個 N: 實線+圓圈 / 點線+圓圈
                marker_every = max(1, len(M_over_N) // 15)
                ax_combined.plot(M_over_N, analytical_N_S, 'k-', linewidth=1.5,
                        marker='o', markersize=5, markevery=marker_every,
                        markerfacecolor='none', markeredgecolor='black', markeredgewidth=1,
                        label=rf'N={N_value} $N_{{S,1}}$/N Analytical Model')
                ax_combined.plot(M_over_N, analytical_N_C, 'k:', linewidth=1.5,
                        marker='o', markersize=5, markevery=marker_every,
                        markerfacecolor='none', markeredgecolor='black', markeredgewidth=1,
                        label=rf'N={N_value} $N_{{C,1}}$/N Analytical Model')
            else:
                # 第二個 N: 實線無標記 / 虛線無標記
                ax_combined.plot(M_over_N, analytical_N_S, 'k-', linewidth=1.5,
                        label=rf'N={N_value} $N_{{S,1}}$/N Analytical Model')
                ax_combined.plot(M_over_N, analytical_N_C, 'k--', linewidth=1.5,
                        label=rf'N={N_value} $N_{{C,1}}$/N Analytical Model')
        
        # 繪製 Approximation: 細點線 / 點劃線
        N_key = available_N_keys[0]
        N_data = data[N_key]
        M_over_N = np.array(N_data['M_over_N'])
        approx_N_S = np.array(N_data['approx_N_S'])
        approx_N_C = np.array(N_data['approx_N_C'])
        
        ax_combined.plot(M_over_N, approx_N_S, color='black', linestyle=':', linewidth=1.5,
                label=r'$N_{S,1}$/N Derived Performance Metric, Eq. (4)')
        ax_combined.plot(M_over_N, approx_N_C, color='black', linestyle='-.', linewidth=1.5,
                label=r'$N_{C,1}$/N Derived Performance Metric, Eq. (5)')
        
        # 添加曲線標註 (帶箭頭) - 只在合併圖中添加
        ax_combined.annotate(r'$N_{C,1}$/N', xy=(4.5, 0.92), xytext=(5.5, 0.85),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'),
                    fontsize=12, ha='center')
        
        ax_combined.annotate(r'$N_{S,1}$/N', xy=(4.5, 0.08), xytext=(5.5, 0.2),
                    arrowprops=dict(arrowstyle='->', connectionstyle='arc3', color='black'),
                    fontsize=12, ha='center')
        
        _setup_axis(ax_combined)
        subplot_label = chr(ord('a') + num_N_values + 1)
        ax_combined.set_title(f'({subplot_label}) All Combined', fontsize=11, pad=10)
        ax_combined.legend(loc='center right', fontsize=8, framealpha=0.9)
    
    # 添加總標題
    n_values_str = ', '.join([str(n) for n in available_N_values])
    fig.suptitle(rf'Fig. 1.   Analytical (N={{{n_values_str}}}) and approximation results of $N_{{S,1}}/N$ and $N_{{C,1}}/N$',
                 fontsize=12, y=0.02)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.08, top=0.95)
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Figure 1 已保存: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def _setup_axis(ax):
    """設置共用的軸樣式"""
    ax.set_xlabel('M/N', fontsize=11)
    ax.set_ylabel(r'RAO$_S$/N', fontsize=11)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1.05)
    ax.set_xticks(np.arange(0, 11, 1))
    ax.set_yticks(np.arange(0, 1.1, 0.1))
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

