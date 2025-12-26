# Input: 依赖analytical和simulation模块加载解析和模拟数据，依赖matplotlib绘图
# Output: 提供plot_figure3、plot_figure4、plot_figure5函数，绘制Figure 3-5图表（理论曲线、模拟结果和误差曲线）
# Position: Figure 3-5绘图模块，负责绘制P_S、T_a、P_C的理论曲线、模拟点和误差曲线
# 一旦我被更新，务必更新我的开头注释，以及所属文件夹的md。

"""
Figure 3, 4, 5 合併繪製模組

- Figure 3: Access Success Probability (P_S) vs N
- Figure 4: Mean Access Delay (T_a) vs N
- Figure 5: Collision Probability (P_C) vs N
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_figure3(analytical_data: dict = None, simulation_data: dict = None, save_path: str = None, show: bool = False):
    """
    繪製 Figure 3 - Access Success Probability
    
    Args:
        analytical_data: 解析數據（包含 N_values, P_S_values）
        simulation_data: 模擬數據（包含 N_values, P_S_values, P_S_error）
        save_path: 保存路徑
        show: 是否顯示圖表
    
    Returns:
        Figure 對象
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    M = None
    I_max = None
    
    # 左 Y 軸：Access Success Probability
    ax1.set_xlabel('N', fontsize=12)
    ax1.set_ylabel('Access Success Probability', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    # 繪製理論曲線（藍色實線）
    if analytical_data:
        ax1.plot(analytical_data['N_values'], analytical_data['P_S_values'], 
                'b-', linewidth=2, label='Derived Performance Metric, Eq. (8)')
        M = analytical_data.get('M')
        I_max = analytical_data.get('I_max')
    
    # 繪製模擬結果（藍色圓圈）
    if simulation_data:
        ax1.plot(simulation_data['N_values'], simulation_data['P_S_values'], 
                'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
                label='Simulation Results')
        M = simulation_data.get('M', M)
        I_max = simulation_data.get('I_max', I_max)
    
    ax1.set_ylim(0, 1.05)
    ax1.set_xlim(5, 45)
    
    # 右 Y 軸：Approximation Error (%)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Approximation Error (%)', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    # 從 simulation_data 讀取預先計算的誤差
    if simulation_data and 'P_S_error' in simulation_data:
        error_values = simulation_data['P_S_error']
        # 過濾掉 None 值
        valid_data = [(n, e) for n, e in zip(simulation_data['N_values'], error_values) if e is not None]
        if valid_data:
            valid_N, valid_error = zip(*valid_data)
            ax2.plot(valid_N, valid_error, 'g--', linewidth=2, label='Approximation Error')
    
    ax2.set_ylim(0, 100)
    
    title = 'Fig. 3. Access success probability and its approximation error.'
    ax1.set_title(title, fontsize=13, fontweight='bold', pad=10)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc='upper left', fontsize=10)
    
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Figure 3 已保存: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def plot_figure4(analytical_data: dict = None, simulation_data: dict = None, save_path: str = None, show: bool = False):
    """
    繪製 Figure 4 - Mean Access Delay
    
    Args:
        analytical_data: 解析數據（包含 N_values, T_a_values）
        simulation_data: 模擬數據（包含 N_values, T_a_values, T_a_error）
        save_path: 保存路徑
        show: 是否顯示圖表
    
    Returns:
        Figure 對象
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    M = None
    I_max = None
    
    # 左 Y 軸：Mean Access Delay
    ax1.set_xlabel('N', fontsize=12)
    ax1.set_ylabel('Mean Access Delay ($T_a$)', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    if analytical_data:
        ax1.plot(analytical_data['N_values'], analytical_data['T_a_values'], 
                'b-', linewidth=2, label='Derived Performance Metric, Eq. (9)')
        M = analytical_data.get('M')
        I_max = analytical_data.get('I_max')
    
    if simulation_data:
        ax1.plot(simulation_data['N_values'], simulation_data['T_a_values'], 
                'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
                label='Simulation Results')
        M = simulation_data.get('M', M)
        I_max = simulation_data.get('I_max', I_max)
    
    ax1.set_xlim(5, 45)
    ax1.set_ylim(0, 10.0)
    
    # 右 Y 軸：Approximation Error (%)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Approximation Error (%)', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    # 從 simulation_data 讀取預先計算的誤差
    if simulation_data and 'T_a_error' in simulation_data:
        error_values = simulation_data['T_a_error']
        # 過濾掉 None 值
        valid_data = [(n, e) for n, e in zip(simulation_data['N_values'], error_values) if e is not None]
        if valid_data:
            valid_N, valid_error = zip(*valid_data)
            ax2.plot(valid_N, valid_error, 'g--', linewidth=2, label='Approximation Error')
    
    ax2.set_ylim(0, 100)
    
    title = 'Fig. 4. Mean access delay and its approximation error.'
    ax1.set_title(title, fontsize=13, fontweight='bold', pad=10)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc='upper right', fontsize=10)
    
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Figure 4 已保存: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def plot_figure5(analytical_data: dict = None, simulation_data: dict = None, save_path: str = None, show: bool = False):
    """
    繪製 Figure 5 - Collision Probability
    
    Args:
        analytical_data: 解析數據（包含 N_values, P_C_values）
        simulation_data: 模擬數據（包含 N_values, P_C_values, P_C_error）
        save_path: 保存路徑
        show: 是否顯示圖表
    
    Returns:
        Figure 對象
    """
    fig, ax1 = plt.subplots(figsize=(10, 6))
    
    M = None
    I_max = None
    
    # 左 Y 軸：Collision Probability
    ax1.set_xlabel('N', fontsize=12)
    ax1.set_ylabel('Collision Probability ($P_C$)', fontsize=12, color='blue')
    ax1.tick_params(axis='y', labelcolor='blue')
    
    if analytical_data:
        ax1.plot(analytical_data['N_values'], analytical_data['P_C_values'], 
                'b-', linewidth=2, label='Derived Performance Metric, Eq. (10)')
        M = analytical_data.get('M')
        I_max = analytical_data.get('I_max')
    
    if simulation_data:
        ax1.plot(simulation_data['N_values'], simulation_data['P_C_values'], 
                'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
                label='Simulation Results')
        M = simulation_data.get('M', M)
        I_max = simulation_data.get('I_max', I_max)
    
    ax1.set_xlim(5, 45)
    ax1.set_ylim(0, 1.0)
    
    # 右 Y 軸：Approximation Error (%)
    ax2 = ax1.twinx()
    ax2.set_ylabel('Approximation Error (%)', fontsize=12, color='green')
    ax2.tick_params(axis='y', labelcolor='green')
    
    # 從 simulation_data 讀取預先計算的誤差
    if simulation_data and 'P_C_error' in simulation_data:
        error_values = simulation_data['P_C_error']
        # 過濾掉 None 值
        valid_data = [(n, e) for n, e in zip(simulation_data['N_values'], error_values) if e is not None]
        if valid_data:
            valid_N, valid_error = zip(*valid_data)
            ax2.plot(valid_N, valid_error, 'g--', linewidth=2, label='Approximation Error')
    
    ax2.set_ylim(0, 2)
    
    title = 'Fig. 5. Collision probability and its approximation error.'
    ax1.set_title(title, fontsize=13, fontweight='bold', pad=10)
    
    lines1, labels1 = ax1.get_legend_handles_labels()
    ax1.legend(lines1, labels1, loc='upper right', fontsize=10)
    
    ax1.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✓ Figure 5 已保存: {save_path}")
    
    if show:
        plt.show()
    
    return fig


def plot_figure345(analytical_data: dict = None, simulation_data: dict = None, save_dir: str = None):
    """
    一次繪製 Figure 3, 4, 5
    
    Args:
        analytical_data: 合併解析數據（包含 N_values, P_S_values, T_a_values, P_C_values）
        simulation_data: 合併模擬數據（包含 N_values, P_S_values, T_a_values, P_C_values）
        save_dir: 保存目錄
    
    Returns:
        tuple: (fig3, fig4, fig5)
    """
    from pathlib import Path
    
    # 準備各個 Figure 的數據
    anal_fig3 = anal_fig4 = anal_fig5 = None
    sim_fig3 = sim_fig4 = sim_fig5 = None
    
    if analytical_data:
        anal_fig3 = {
            'N_values': analytical_data['N_values'],
            'P_S_values': analytical_data['P_S_values'],
            'M': analytical_data.get('M'),
            'I_max': analytical_data.get('I_max'),
        }
        anal_fig4 = {
            'N_values': analytical_data['N_values'],
            'T_a_values': analytical_data['T_a_values'],
            'M': analytical_data.get('M'),
            'I_max': analytical_data.get('I_max'),
        }
        anal_fig5 = {
            'N_values': analytical_data['N_values'],
            'P_C_values': analytical_data['P_C_values'],
            'M': analytical_data.get('M'),
            'I_max': analytical_data.get('I_max'),
        }
    
    if simulation_data:
        sim_fig3 = {
            'N_values': simulation_data['N_values'],
            'P_S_values': simulation_data['P_S_values'],
            'M': simulation_data.get('M'),
            'I_max': simulation_data.get('I_max'),
        }
        sim_fig4 = {
            'N_values': simulation_data['N_values'],
            'T_a_values': simulation_data['T_a_values'],
            'M': simulation_data.get('M'),
            'I_max': simulation_data.get('I_max'),
        }
        sim_fig5 = {
            'N_values': simulation_data['N_values'],
            'P_C_values': simulation_data['P_C_values'],
            'M': simulation_data.get('M'),
            'I_max': simulation_data.get('I_max'),
        }
    
    # 設定保存路徑
    save_path3 = save_path4 = save_path5 = None
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_path3 = str(save_dir / 'figure3.png')
        save_path4 = str(save_dir / 'figure4.png')
        save_path5 = str(save_dir / 'figure5.png')
    
    # 繪製
    fig3 = plot_figure3(anal_fig3, sim_fig3, save_path3)
    fig4 = plot_figure4(anal_fig4, sim_fig4, save_path4)
    fig5 = plot_figure5(anal_fig5, sim_fig5, save_path5)
    
    return fig3, fig4, fig5
