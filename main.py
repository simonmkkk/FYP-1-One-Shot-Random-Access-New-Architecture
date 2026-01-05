#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One-Shot Random Access 模擬與分析系統 - 主程式入口

支援 CLI 命令和互動式選單兩種操作模式。

Input: config 配置模組, analytical/simulation/plot 各功能模組
Output: 運行解析計算、蒙特卡洛模擬、繪圖、完整流程
Position: 系統入口點，協調所有模組的調用

用法:
    python main.py                           # 互動式選單
    python main.py analytical figure1        # 運行 Figure 1 解析
    python main.py simulation figure345      # 運行 Figure 3, 4, 5 模擬
    python main.py plot figure1              # 繪製 Figure 1
    python main.py run figure1               # 完整流程
    python main.py run figure1 --performance # 啟用性能監測

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

import sys
import argparse
from datetime import datetime
from pathlib import Path

# 添加項目根目錄到路徑
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from config import load_config
from performance import SimpleTimer
from analytical.figure_analysis import (
    run_figure1_analysis,
    run_figure2_analysis,
    run_figure345_analysis,
    load_figure1_results,
    load_figure2_results,
    load_figure345_results,
)
from simulation.figure_simulation import (
    run_figure345_simulation,
    load_figure345_simulation_results,
)
from plot import (
    plot_figure1,
    plot_figure2,
    plot_figure3,
    plot_figure4,
    plot_figure5,
)

# 全局性能監測狀態
_performance_enabled = False


# ============================================================================
# 輔助函數
# ============================================================================

def get_result_dir(result_type: str, figure_name: str) -> Path:
    """獲取結果輸出目錄"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / result_type / figure_name / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    return result_dir


def _get_analytical_data_for_figure(figure_name: str):
    """從 figure345 合併結果讀取指定 Figure 的解析數據"""
    combined = load_figure345_results()
    if combined is None:
        return None
    
    if figure_name == 'figure3':
        return {
            'N_values': combined['N_values'],
            'P_S_values': combined['P_S_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
    elif figure_name == 'figure4':
        return {
            'N_values': combined['N_values'],
            'T_a_values': combined['T_a_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
    elif figure_name == 'figure5':
        return {
            'N_values': combined['N_values'],
            'P_C_values': combined['P_C_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
    return None


def _get_simulation_data_for_figure(figure_name: str):
    """從 figure345 合併結果讀取指定 Figure 的模擬數據（包含 Approximation Error）"""
    combined = load_figure345_simulation_results()
    if combined is None:
        return None
    
    if figure_name == 'figure3':
        result = {
            'N_values': combined['N_values'],
            'P_S_values': combined['P_S_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
        if 'P_S_error' in combined:
            result['P_S_error'] = combined['P_S_error']
        return result
    elif figure_name == 'figure4':
        result = {
            'N_values': combined['N_values'],
            'T_a_values': combined['T_a_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
        if 'T_a_error' in combined:
            result['T_a_error'] = combined['T_a_error']
        return result
    elif figure_name == 'figure5':
        result = {
            'N_values': combined['N_values'],
            'P_C_values': combined['P_C_values'],
            'M': combined['M'],
            'I_max': combined['I_max'],
        }
        if 'P_C_error' in combined:
            result['P_C_error'] = combined['P_C_error']
        return result
    return None


# ============================================================================
# 【解析計算 (Analytical)】
#    1. Figure 1: NS,1/N & NC,1/N 精確公式 + 近似公式
#    2. Figure 2: 近似誤差分析（精確 vs 近似）
#    3. Figure 3, 4, 5 合併解析 (P_S, T_a, P_C)
#    4. 運行所有解析計算
# ============================================================================

def run_analytical_figure1(timer: SimpleTimer = None):
    """[選項 1] Figure 1: NS,1/N & NC,1/N 精確公式 + 近似公式"""
    config = load_config('analytical', 'figure1')
    run_figure1_analysis(config)


def run_analytical_figure2(timer: SimpleTimer = None):
    """[選項 2] Figure 2: 近似誤差分析（精確 vs 近似）
    
    Note: Figure 2 使用 Figure 1 的配置，因為兩者基於相同的運算。
    """
    config = load_config('analytical', 'figure1')  # 使用 Figure 1 配置
    run_figure2_analysis(config)


def run_analytical_figure345(timer: SimpleTimer = None):
    """[選項 3] Figure 3, 4, 5 合併解析 (P_S, T_a, P_C)"""
    config = load_config('analytical', 'figure345')
    run_figure345_analysis(config)


def run_analytical_all(timer: SimpleTimer = None):
    """[選項 4] 運行所有解析計算"""
    print(f"\n{'='*60}")
    print("正在運行 Figure 1 解析計算...")
    print(f"{'='*60}")
    config = load_config('analytical', 'figure1')
    fig1_data = run_figure1_analysis(config)
    
    print(f"\n{'='*60}")
    print("正在運行 Figure 2 解析計算 (使用 Figure 1 結果)...")
    print(f"{'='*60}")
    # 直接傳入 Figure 1 的結果，避免重複運算
    run_figure2_analysis(config, fig1_data=fig1_data)
    
    print(f"\n{'='*60}")
    print("正在運行 Figure 3, 4, 5 合併解析計算...")
    print(f"{'='*60}")
    run_analytical_figure345()


# ============================================================================
# 【模擬 (Simulation)】
#    5. Figure 3, 4, 5 合併模擬 (P_S, T_a, P_C)
# ============================================================================

def run_simulation_figure345(timer: SimpleTimer = None):
    """[選項 5] Figure 3, 4, 5 合併模擬 (P_S, T_a, P_C)"""
    config = load_config('simulation', 'figure345')
    run_figure345_simulation(config)


# ============================================================================
# 【繪圖 (Plot)】
#    6. 繪製 Figure 1
#    7. 繪製 Figure 2
#    8. 繪製 Figure 3, 4, 5
#    9. 繪製所有圖表
# ============================================================================

def run_plot_figure1(show: bool = True, timer: SimpleTimer = None):
    """【選項 6】繪製 Figure 1"""
    print("從 CSV 讀取 Figure 1 數據...")
    data = load_figure1_results()
    if data is None:
        print("❌ 無法找到 Figure 1 數據。請先運行選項 1 進行解析計算。")
        return
    
    result_dir = get_result_dir('graph', 'figure1')
    save_path = result_dir / "figure1.png"
    plot_figure1(data, data_type='analytical', save_path=str(save_path), show=show)


def run_plot_figure2(show: bool = True, timer: SimpleTimer = None):
    """【選項 7】繪製 Figure 2"""
    print("從 CSV 讀取 Figure 2 數據...")
    data = load_figure2_results()
    if data is None:
        print("❌ 無法找到 Figure 2 數據。請先運行選項 2 進行解析計算。")
        return
    
    result_dir = get_result_dir('graph', 'figure2')
    save_path = result_dir / "figure2.png"
    plot_figure2(data, save_path=str(save_path), show=show)


def run_plot_figure345(show: bool = True, timer: SimpleTimer = None):
    """[選項 8] 繪製 Figure 3, 4, 5"""
    # Figure 3
    print("從 CSV 讀取 Figure 3 數據...")
    analytical_data = _get_analytical_data_for_figure('figure3')
    simulation_data = _get_simulation_data_for_figure('figure3')
    if analytical_data is None and simulation_data is None:
        print("❌ 無法找到 Figure 3 數據。請先運行選項 3 進行解析計算或選項 5 進行模擬。")
    else:
        result_dir = get_result_dir('graph', 'figure3')
        save_path = result_dir / "figure3.png"
        plot_figure3(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=False)
    
    # Figure 4
    print("從 CSV 讀取 Figure 4 數據...")
    analytical_data = _get_analytical_data_for_figure('figure4')
    simulation_data = _get_simulation_data_for_figure('figure4')
    if analytical_data is None and simulation_data is None:
        print("❌ 無法找到 Figure 4 數據。請先運行選項 3 進行解析計算或選項 5 進行模擬。")
    else:
        result_dir = get_result_dir('graph', 'figure4')
        save_path = result_dir / "figure4.png"
        plot_figure4(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=False)
    
    # Figure 5
    print("從 CSV 讀取 Figure 5 數據...")
    analytical_data = _get_analytical_data_for_figure('figure5')
    simulation_data = _get_simulation_data_for_figure('figure5')
    if analytical_data is None and simulation_data is None:
        print("❌ 無法找到 Figure 5 數據。請先運行選項 3 進行解析計算或選項 5 進行模擬。")
    else:
        result_dir = get_result_dir('graph', 'figure5')
        save_path = result_dir / "figure5.png"
        plot_figure5(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=show)


def run_plot_all(timer: SimpleTimer = None):
    """【選項 9】繪製所有圖表"""
    print("\n正在繪製 Figure 1...")
    run_plot_figure1(show=False)
    
    print("\n正在繪製 Figure 2...")
    run_plot_figure2(show=False)
    
    print("\n正在繪製 Figure 3, 4, 5...")
    run_plot_figure345(show=True)


# ============================================================================
# 【完整流程】
#   10. Figure 1 完整流程 (Analytical + Plot)
#   11. Figure 2 完整流程 (Analytical + Plot)
#   12. Figure 3, 4, 5 完整流程 (Analytical + Simulation + Plot)
#   13. 所有圖表完整流程
# ============================================================================

def run_pipeline_figure1(timer: SimpleTimer = None):
    """[選項 10] Figure 1 完整流程 (Analytical + Plot)"""
    print(f"\n{'='*60}")
    print("開始 Figure 1 完整流程")
    print(f"{'='*60}")
    
    print(f"\n[1/2] 運行解析計算（精確公式 + 近似公式）...")
    if timer:
        with timer.step("解析計算"):
            config = load_config('analytical', 'figure1')
            run_figure1_analysis(config, timer=timer)
    else:
        run_analytical_figure1()
    
    print(f"\n[2/2] 繪製圖表...")
    if timer:
        with timer.step("繪圖"):
            run_plot_figure1(show=True)
    else:
        run_plot_figure1()
    
    print(f"\n{'='*60}")
    print("Figure 1 完整流程完成!")
    print(f"{'='*60}")


def run_pipeline_figure2(timer: SimpleTimer = None):
    """[選項 11] Figure 2 完整流程 (Analytical + Plot)"""
    print(f"\n{'='*60}")
    print("開始 Figure 2 完整流程")
    print(f"{'='*60}")
    
    print(f"\n[1/2] 運行解析計算（精確 vs 近似誤差）...")
    if timer:
        with timer.step("解析計算"):
            config = load_config('analytical', 'figure1')
            run_figure2_analysis(config, timer=timer)
    else:
        run_analytical_figure2()
    
    print(f"\n[2/2] 繪製圖表...")
    if timer:
        with timer.step("繪圖"):
            run_plot_figure2(show=True)
    else:
        run_plot_figure2()
    
    print(f"\n{'='*60}")
    print("Figure 2 完整流程完成!")
    print(f"{'='*60}")


def run_pipeline_figure345(timer: SimpleTimer = None):
    """[選項 12] Figure 3, 4, 5 完整流程 (Analytical + Simulation + Plot)"""
    print(f"\n{'='*60}")
    print("開始 Figure 3, 4, 5 完整流程")
    print(f"{'='*60}")
    
    print(f"\n[1/3] 運行 Figure 3, 4, 5 合併解析計算...")
    if timer:
        with timer.step("解析計算"):
            config = load_config('analytical', 'figure345')
            run_figure345_analysis(config, timer=timer)
    else:
        run_analytical_figure345()
    
    print(f"\n[2/3] 運行 Figure 3, 4, 5 合併模擬...")
    if timer:
        with timer.step("模擬"):
            config = load_config('simulation', 'figure345')
            run_figure345_simulation(config, timer=timer)
    else:
        run_simulation_figure345()
    
    print(f"\n[3/3] 繪製圖表...")
    if timer:
        with timer.step("繪圖"):
            run_plot_figure345(show=True)
    else:
        run_plot_figure345()
    
    print(f"\n{'='*60}")
    print("Figure 3, 4, 5 完整流程完成!")
    print(f"{'='*60}")


def run_pipeline_all(timer: SimpleTimer = None):
    """[選項 13] 所有圖表完整流程"""
    # Note: 當運行所有流程時，每個子流程會分別顯示性能報告
    run_pipeline_figure1(timer=None)
    run_pipeline_figure2(timer=None)
    run_pipeline_figure345(timer=None)


# ============================================================================
# 互動式選單
# ============================================================================

def print_menu():
    """打印選單"""
    print("\n" + "=" * 70)
    print("One-Shot Random Access 模擬與分析系統")
    print("=" * 70)
    print("\n請選擇操作:\n")
    
    print("【解析計算 (Analytical)】")
    print("   1. Figure 1: NS,1/N & NC,1/N 精確公式 + 近似公式")
    print("   2. Figure 2: 近似誤差分析（精確 vs 近似）")
    print("   3. Figure 3, 4, 5 合併解析 (P_S, T_a, P_C)")
    print("   4. 運行所有解析計算")
    
    print("\n【模擬 (Simulation)】")
    print("   5. Figure 3, 4, 5 合併模擬 (P_S, T_a, P_C)")
    
    print("\n【繪圖 (Plot)】")
    print("   6. 繪製 Figure 1")
    print("   7. 繪製 Figure 2")
    print("   8. 繪製 Figure 3, 4, 5")
    print("   9. 繪製所有圖表")
    
    print("\n【完整流程】")
    print("  10. Figure 1 完整流程 (Analytical + Plot)")
    print("  11. Figure 2 完整流程 (Analytical + Plot)")
    print("  12. Figure 3, 4, 5 完整流程 (Analytical + Simulation + Plot)")
    print("  13. 所有圖表完整流程")
    
    # 顯示性能監測狀態
    status = "✅ 已開啟" if _performance_enabled else "❌ 已關閉"
    print(f"\n【設定】")
    print(f"   p. 切換性能監測 ({status})")
    
    print("\n   0. 退出")
    print("=" * 70)


def _run_with_performance(func, name: str):
    """包裝函數以支持性能監測"""
    global _performance_enabled
    
    if _performance_enabled:
        timer = SimpleTimer(name)
        print("📊 性能監測已啟用\n")
        try:
            func(timer=timer)
        finally:
            timer.print_report()
            timer.save_json(str(PROJECT_ROOT / 'result' / 'performance'))
    else:
        func()


def interactive_menu():
    """互動式選單"""
    global _performance_enabled
    
    while True:
        print_menu()
        
        try:
            choice = input("\n請輸入選項: ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print("\n再見!")
            break
        
        if choice == '0':
            print("\n再見!")
            break
        
        # 【設定】切換性能監測
        elif choice == 'p':
            _performance_enabled = not _performance_enabled
            status = "已開啟 ✅" if _performance_enabled else "已關閉 ❌"
            print(f"\n📊 性能監測 {status}")
            continue
        
        # 【解析計算 (Analytical)】 1-4
        elif choice == '1':
            _run_with_performance(run_analytical_figure1, "Figure 1 解析計算")
        elif choice == '2':
            _run_with_performance(run_analytical_figure2, "Figure 2 解析計算")
        elif choice == '3':
            _run_with_performance(run_analytical_figure345, "Figure 3,4,5 解析計算")
        elif choice == '4':
            _run_with_performance(run_analytical_all, "所有解析計算")
        
        # 【模擬 (Simulation)】 5
        elif choice == '5':
            _run_with_performance(run_simulation_figure345, "Figure 3,4,5 模擬")
        
        # 【繪圖 (Plot)】 6-9
        elif choice == '6':
            _run_with_performance(run_plot_figure1, "Figure 1 繪圖")
        elif choice == '7':
            _run_with_performance(run_plot_figure2, "Figure 2 繪圖")
        elif choice == '8':
            _run_with_performance(run_plot_figure345, "Figure 3,4,5 繪圖")
        elif choice == '9':
            _run_with_performance(run_plot_all, "所有繪圖")
        
        # 【完整流程】 10-13
        elif choice == '10':
            _run_with_performance(run_pipeline_figure1, "Figure 1 完整流程")
        elif choice == '11':
            _run_with_performance(run_pipeline_figure2, "Figure 2 完整流程")
        elif choice == '12':
            _run_with_performance(run_pipeline_figure345, "Figure 3,4,5 完整流程")
        elif choice == '13':
            _run_with_performance(run_pipeline_all, "所有完整流程")
        
        else:
            print("\n無效選項，請重新輸入")


# ============================================================================
# CLI 處理
# ============================================================================

def parse_args():
    """解析命令行參數"""
    parser = argparse.ArgumentParser(
        description='One-Shot Random Access 模擬與分析系統',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
範例:
  python main.py                           # 互動式選單
  python main.py analytical figure1        # 運行 Figure 1 解析
  python main.py analytical figure345      # 運行 Figure 3, 4, 5 解析
  python main.py analytical all            # 運行所有解析
  python main.py simulation figure345      # 運行 Figure 3, 4, 5 模擬
  python main.py plot figure1              # 繪製 Figure 1
  python main.py plot figure345            # 繪製 Figure 3, 4, 5
  python main.py plot all                  # 繪製所有圖表
  python main.py run figure1               # Figure 1 完整流程
  python main.py run figure345             # Figure 3, 4, 5 完整流程
  python main.py run all                   # 所有完整流程
  python main.py run figure1 --performance # 啟用性能監測
        """
    )
    parser.add_argument(
        'command',
        nargs='?',
        choices=['analytical', 'simulation', 'plot', 'run'],
        help='命令: analytical, simulation, plot, run'
    )
    parser.add_argument(
        'target',
        nargs='?',
        help='目標: figure1, figure2, figure345, all'
    )
    parser.add_argument(
        '--performance',
        action='store_true',
        help='啟用性能監測'
    )
    parser.add_argument(
        '--performance-report',
        type=str,
        default=None,
        help='性能報告輸出目錄'
    )
    return parser.parse_args()


def main():
    """主函數"""
    args = parse_args()
    
    # 如果沒有命令，進入互動式選單
    if args.command is None:
        interactive_menu()
        return
    
    # 啟用性能監測
    if args.performance:
        from performance import start_monitoring, stop_monitoring, generate_performance_report
        start_monitoring()
        print("📊 性能監測已啟用")
    
    # CLI 模式
    command = args.command
    target = args.target
    
    if target is None:
        print("請指定目標 (figure1, figure2, figure345, all)")
        return
    
    try:
        # analytical 命令
        if command == 'analytical':
            if target == 'figure1':
                run_analytical_figure1()
            elif target == 'figure2':
                run_analytical_figure2()
            elif target == 'figure345':
                run_analytical_figure345()
            elif target == 'all':
                run_analytical_all()
            else:
                print(f"未知的目標: {target}")
                print("支援的目標: figure1, figure2, figure345, all")
        
        # simulation 命令
        elif command == 'simulation':
            if target == 'figure345' or target == 'all':
                run_simulation_figure345()
            elif target in ['figure1', 'figure2']:
                print(f"錯誤: {target} 不需要模擬（只有 Analytical vs Approximation 對比）")
                print("請使用: python main.py simulation figure345")
            else:
                print(f"未知的目標: {target}")
                print("請使用: python main.py simulation figure345")
        
        # plot 命令
        elif command == 'plot':
            if target == 'figure1':
                run_plot_figure1()
            elif target == 'figure2':
                run_plot_figure2()
            elif target == 'figure345':
                run_plot_figure345()
            elif target == 'all':
                run_plot_all()
            else:
                print(f"未知的目標: {target}")
                print("支援的目標: figure1, figure2, figure345, all")
        
        # run 命令
        elif command == 'run':
            if target == 'figure1':
                run_pipeline_figure1()
            elif target == 'figure2':
                run_pipeline_figure2()
            elif target == 'figure345':
                run_pipeline_figure345()
            elif target == 'all':
                run_pipeline_all()
            else:
                print(f"未知的目標: {target}")
                print("支援的目標: figure1, figure2, figure345, all")
    
    finally:
        # 生成性能報告
        if args.performance:
            stop_monitoring()
            output_dir = args.performance_report or str(PROJECT_ROOT / 'result' / 'performance')
            generate_performance_report(output_dir=output_dir)


if __name__ == "__main__":
    main()

