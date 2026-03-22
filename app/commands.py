#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Commands - Analytical, Simulation, Plot, and Pipeline functions
# for One-Shot Random Access analysis.
#
# Run directory layout:
#   • Standalone runs → result/<category>/<name>/<timestamp>/
#   • Pipeline runs   → result/<category>/<name>/<timestamp>/
# ============================================================================

import sys
import time
import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.display import (
    _print_output_path,
    _print_analytical_params,
    _print_simulation_params,
    _confirm_run,
)

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))


# ============================================================================
# Helper Functions
# ============================================================================

def get_result_dir(result_type: str, figure_name: str) -> Path:
    """Get the output directory for results."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_dir = PROJECT_ROOT / 'result' / result_type / figure_name / timestamp
    result_dir.mkdir(parents=True, exist_ok=True)
    return result_dir


def _get_analytical_data_for_figure(figure_name: str):
    """Read analytical data for a specific figure from combined figure345 results."""
    try:
        from analytical.figure_analysis import load_figure345_results
    except (ModuleNotFoundError, ImportError):
        return None

    combined = load_figure345_results()
    if combined is None:
        return None

    key_map = {
        'figure3': 'P_S_values',
        'figure4': 'T_a_values',
        'figure5': 'P_C_values',
    }
    value_key = key_map.get(figure_name)
    if not value_key:
        return None

    return {
        'N_values': combined['N_values'],
        value_key: combined[value_key],
        'M': combined['M'],
        'I_max': combined['I_max'],
    }


def _get_simulation_data_for_figure(figure_name: str):
    """Read simulation data for a specific figure."""
    try:
        from simulation.core.runner import PROJECT_ROOT as SIM_PROJECT_ROOT
    except (ModuleNotFoundError, ImportError):
        return None

    sim_result_dir = SIM_PROJECT_ROOT / "result" / "simulation" / "figure345"
    if not sim_result_dir.exists():
        return None

    timestamp_dirs = [d for d in sim_result_dir.iterdir() if d.is_dir()]
    if not timestamp_dirs:
        return None

    latest_dir = max(timestamp_dirs, key=lambda d: d.stat().st_mtime)
    csv_files = list(latest_dir.glob("*.csv"))
    if not csv_files:
        return None

    csv_path = csv_files[0]
    combined = {'N_values': [], 'P_S_values': [], 'T_a_values': [], 'P_C_values': []}

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            combined['N_values'].append(int(row['N']))
            combined['P_S_values'].append(float(row['P_S']))
            combined['T_a_values'].append(float(row['T_a']))
            combined['P_C_values'].append(float(row['P_C']))

    combined['M'] = 100
    combined['I_max'] = 10

    key_map = {
        'figure3': 'P_S_values',
        'figure4': 'T_a_values',
        'figure5': 'P_C_values',
    }
    value_key = key_map.get(figure_name)
    if not value_key:
        return None

    return {
        'N_values': combined['N_values'],
        value_key: combined[value_key],
        'M': combined['M'],
        'I_max': combined['I_max'],
    }


# ============================================================================
# [Analytical] Functions
# ============================================================================

def run_analytical_figure1(*, _step: str = ""):
    """
    Analytical: Figure 1 — NS,1/N & NC,1/N exact + approximate formulas.
    """
    try:
        from configs import load_config
        from analytical.figure_analysis import run_figure1_analysis
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('analytical', 'figure1')

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Running Analysis: Figure 1 (NS,1/N & NC,1/N)")
    print("------ Analytical Configuration ------")
    print(f"  [N Values]")
    print(f"  N = {config['n_values']}")
    print(f"  M/N max = {config['m_over_n_max']}")
    print("--------------------------------------")
    print()

    if not _step:
        if not _confirm_run():
            return False

    result = run_figure1_analysis(config)
    print("Figure 1 analysis completed.")
    return result


def run_analytical_figure2(*, _step: str = ""):
    """
    Analytical: Figure 2 — Approximation Error (exact vs approximate).
    """
    try:
        from configs import load_config
        from analytical.figure_analysis import run_figure1_analysis, run_figure2_analysis
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('analytical', 'figure1')

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Running Analysis: Figure 2 (Approximation Error)")
    print("------ Analytical Configuration ------")
    print(f"  [N Values]")
    print(f"  N = {config['n_values']}")
    print(f"  M/N max = {config['m_over_n_max']}")
    print("--------------------------------------")
    print()

    if not _step:
        if not _confirm_run():
            return False

    run_figure2_analysis(config)
    print("Figure 2 analysis completed.")


def run_analytical_figure345(*, _step: str = ""):
    """
    Analytical: Figure 3, 4, 5 combined analysis (P_S, T_a, P_C).
    """
    try:
        from configs import load_config
        from analytical.figure_analysis import run_figure345_analysis
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('analytical', 'figure345')

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Running Analysis: Figure 3, 4, 5 (P_S, T_a, P_C)")
    _print_analytical_params(
        M=config['M'],
        I_max=config['I_max'],
        N_values=list(range(config['N_start'], config['N_stop'], config['N_step'])),
        figure_name="Figure 3, 4, 5",
    )

    if not _step:
        if not _confirm_run():
            return False

    run_figure345_analysis(config)
    print("Figure 3, 4, 5 analysis completed.")


def run_analytical_all():
    """Run all analytical computations."""
    try:
        from configs import load_config
        from analytical.figure_analysis import run_figure1_analysis, run_figure2_analysis
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('analytical', 'figure1')

    print("\n[1/3]")
    print("Running Analysis: Figure 1 (NS,1/N & NC,1/N)")
    fig1_data = run_figure1_analysis(config)
    print()

    print("[2/3]")
    print("Running Analysis: Figure 2 (Approximation Error)")
    run_figure2_analysis(config, fig1_data=fig1_data)
    print()

    run_analytical_figure345(_step="[3/3]")


# ============================================================================
# [Simulation] Functions
# ============================================================================

def run_simulation_figure345(*, _step: str = ""):
    """
    Simulation: Figure 3, 4, 5 combined simulation (P_S, T_a, P_C).
    """
    try:
        from simulation.core.config import Config
        from simulation.core.runner import run_experiment
        from configs import load_config
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('simulation', 'figure345')
    sim = config.get('simulation', {})

    # Parse n_values (supports range string "10-300:10", list, or int)
    from simulation.core.config import Config
    n_values = Config.parse_n_values(config.get('n_values', []))

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Running Simulation: Figure 3, 4, 5 (P_S, T_a, P_C)")
    _print_simulation_params(
        M=sim.get('M', 100),
        I_max=sim.get('I_max', 10),
        N_values=n_values,
        num_samples=sim.get('num_samples', 10000),
        num_workers=sim.get('num_workers', -1),
    )

    if not _step:
        if not _confirm_run():
            return False

    # Use the configs path
    from configs.loader import CONFIGS_ROOT
    config_path = CONFIGS_ROOT / "simulation" / "config_figure345.yaml"
    run_experiment(config_path)
    print("Figure 3, 4, 5 simulation completed.")


def run_simulation_ue_sweep(*, _step: str = ""):
    """
    Simulation: UE Sweep — P_S, T_a, P_C vs M (fixed N).
    """
    try:
        from simulation.core.config import Config
        from simulation.core.runner import run_experiment
        from configs import load_config
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    config = load_config('simulation', 'ue_sweep')
    sim = config.get('simulation', {})

    # Parse m_values (supports range string "10-300:10", list, or int)
    m_values = Config.parse_n_values(config.get('m_values', []))

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Running Simulation: UE Sweep (P_S, T_a, P_C vs M)")
    print("------ Simulation Configuration ------")
    print("  [Parameters]")
    print(f"  N={sim.get('N', 50)} (fixed), I_max={sim.get('I_max', 10)}")
    print()
    print("  [M Values (UE count)]")
    print(f"  M = {list(m_values)}")
    print()
    print("  [Monte Carlo]")
    print(f"  num_samples = {sim.get('num_samples', 10000):,}")
    print("--------------------------------------")
    print()

    if not _step:
        if not _confirm_run():
            return False

    from configs.loader import CONFIGS_ROOT
    config_path = CONFIGS_ROOT / "simulation" / "config_ue_sweep.yaml"
    run_experiment(config_path)
    print("UE Sweep simulation completed.")


# ============================================================================
# [Plot] Functions
# ============================================================================

def run_plot_figure1(*, _step: str = "", show: bool = True):
    """
    Plot: Figure 1.
    """
    try:
        from analytical.figure_analysis import load_figure1_results
        from plot import plot_figure1
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Plotting: Figure 1")

    data = load_figure1_results()
    if data is None:
        print("No Figure 1 data found. Please run analytical option 1 first.")
        return

    result_dir = get_result_dir('graph', 'figure1')
    save_path = result_dir / "figure1.png"
    plot_figure1(data, data_type='analytical', save_path=str(save_path), show=show)
    _print_output_path(save_path)
    print("Figure 1 plot completed.")


def run_plot_figure2(*, _step: str = "", show: bool = True):
    """
    Plot: Figure 2.
    """
    try:
        from analytical.figure_analysis import load_figure2_results
        from plot import plot_figure2
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Plotting: Figure 2")

    data = load_figure2_results()
    if data is None:
        print("No Figure 2 data found. Please run analytical option 2 first.")
        return

    result_dir = get_result_dir('graph', 'figure2')
    save_path = result_dir / "figure2.png"
    plot_figure2(data, save_path=str(save_path), show=show)
    _print_output_path(save_path)
    print("Figure 2 plot completed.")


def run_plot_figure345(*, _step: str = "", show: bool = True):
    """
    Plot: Figure 3, 4, 5.
    """
    try:
        from plot import plot_figure3, plot_figure4, plot_figure5
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Plotting: Figure 3, 4, 5")

    # Figure 3
    analytical_data = _get_analytical_data_for_figure('figure3')
    simulation_data = _get_simulation_data_for_figure('figure3')
    if analytical_data is None and simulation_data is None:
        print("No Figure 3 data found. Please run option 3 or option 5 first.")
    else:
        result_dir = get_result_dir('graph', 'figure3')
        save_path = result_dir / "figure3.png"
        plot_figure3(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=False)
        _print_output_path(save_path)

    # Figure 4
    analytical_data = _get_analytical_data_for_figure('figure4')
    simulation_data = _get_simulation_data_for_figure('figure4')
    if analytical_data is None and simulation_data is None:
        print("No Figure 4 data found. Please run option 3 or option 5 first.")
    else:
        result_dir = get_result_dir('graph', 'figure4')
        save_path = result_dir / "figure4.png"
        plot_figure4(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=False)
        _print_output_path(save_path)

    # Figure 5
    analytical_data = _get_analytical_data_for_figure('figure5')
    simulation_data = _get_simulation_data_for_figure('figure5')
    if analytical_data is None and simulation_data is None:
        print("No Figure 5 data found. Please run option 3 or option 5 first.")
    else:
        result_dir = get_result_dir('graph', 'figure5')
        save_path = result_dir / "figure5.png"
        plot_figure5(analytical_data=analytical_data, simulation_data=simulation_data, save_path=str(save_path), show=show)
        _print_output_path(save_path)

    print("Figure 3, 4, 5 plots completed.")


def run_plot_ue_sweep(*, _step: str = "", show: bool = True):
    """
    Plot: UE Sweep (P_S, T_a, P_C vs M).
    """
    try:
        from plot.ue_sweep import load_ue_sweep_results, plot_ue_sweep_all
    except (ModuleNotFoundError, ImportError) as e:
        raise SystemExit(f"Missing dependency: {e}") from e

    step_line = f"\n{_step}\n" if _step else "\n"
    print(f"{step_line}Plotting: UE Sweep (P_S, T_a, P_C vs M)")

    data = load_ue_sweep_results()
    if data is None:
        print("No UE Sweep data found. Please run option 6 first.")
        return

    result_dir = get_result_dir('graph', 'ue_sweep')
    plot_ue_sweep_all(data, save_dir=str(result_dir), show=show)
    _print_output_path(result_dir)
    print("UE Sweep plots completed.")


def run_plot_all(show: bool = True):
    """
    Plot all figures (sequential).
    """
    print("\nPlotting: All Figures")
    run_plot_figure1(show=False)
    print()
    run_plot_figure2(show=False)
    print()
    run_plot_figure345(show=False)
    print()
    run_plot_ue_sweep(show=show)
    print("\nAll plots completed.")


# ============================================================================
# [Pipeline] Functions (Analytical + Simulation + Plot)
# ============================================================================

def run_pipeline_figure1():
    """
    Pipeline: Figure 1 (Analytical + Plot).
    """
    print("\nOrder: Analytical → Plot")

    run_analytical_figure1(_step="[1/2]")
    print()
    run_plot_figure1(_step="[2/2]", show=False)

    print("\nFigure 1 pipeline completed.")


def run_pipeline_figure2():
    """
    Pipeline: Figure 2 (Analytical + Plot).
    """
    print("\nOrder: Analytical → Plot")

    run_analytical_figure2(_step="[1/2]")
    print()
    run_plot_figure2(_step="[2/2]", show=False)

    print("\nFigure 2 pipeline completed.")


def run_pipeline_figure345():
    """
    Pipeline: Figure 3, 4, 5 (Analytical + Simulation + Plot).
    """
    print("\nOrder: Analytical → Simulation → Plot")

    run_analytical_figure345(_step="[1/3]")
    print()
    run_simulation_figure345(_step="[2/3]")
    print()
    run_plot_figure345(_step="[3/3]", show=False)

    print("\nFigure 3, 4, 5 pipeline completed.")


def run_pipeline_ue_sweep():
    """
    Pipeline: UE Sweep (Simulation + Plot).
    """
    print("\nOrder: Simulation → Plot")

    run_simulation_ue_sweep(_step="[1/2]")
    print()
    run_plot_ue_sweep(_step="[2/2]", show=False)

    print("\nUE Sweep pipeline completed.")


def run_pipeline_all():
    """
    Full pipeline for all figures.
    """
    print("\nFigure 1")
    run_pipeline_figure1()

    print("\nFigure 2")
    run_pipeline_figure2()

    print("\nFigure 3, 4, 5")
    run_pipeline_figure345()

    print("\nUE Sweep")
    run_pipeline_ue_sweep()

    print("\nFull pipeline completed.")

