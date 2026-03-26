# ============================================================================
# UE Sweep Plots — P_S, T_a, P_C vs M (fixed N)
# ============================================================================

import csv
from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
from simulation.core.paths import SIMULATION_ROOT

# Backend setup
matplotlib.use('Agg')


# ============================================================================
# Data loading
# ============================================================================

def load_ue_sweep_results(result_dir: str = None) -> dict | None:
    """
    Load UE sweep simulation results from the latest CSV.

    Returns:
        dict with M_values, P_S_values, T_a_values, P_C_values, N, I_max.
    """
    if result_dir is None:
        # Unified run path: result/runs/simulation/ue_sweep/<timestamp>/
        result_dir = SIMULATION_ROOT / "ue_sweep"

    result_dir = Path(result_dir)
    if not result_dir.exists():
        return None

    # Find latest timestamp directory
    timestamp_dirs = [d for d in result_dir.iterdir() if d.is_dir()]
    if not timestamp_dirs:
        return None

    latest_dir = max(timestamp_dirs, key=lambda d: d.stat().st_mtime)
    csv_files = list(latest_dir.glob("*.csv"))
    if not csv_files:
        return None

    data = {
        'M_values': [], 'P_S_values': [], 'T_a_values': [], 'P_C_values': [],
        'N': None, 'I_max': None,
    }

    with open(csv_files[0], 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data['M_values'].append(int(row['M']))
            data['P_S_values'].append(float(row['P_S']))
            data['T_a_values'].append(float(row['T_a']))
            data['P_C_values'].append(float(row['P_C']))
            if data['N'] is None:
                data['N'] = int(row['N'])
            if data['I_max'] is None:
                data['I_max'] = int(row['I_max'])

    return data if data['M_values'] else None


# ============================================================================
# Plot functions
# ============================================================================

def plot_ue_sweep_ps(data: dict, *, save_path: str = None, show: bool = False):
    """
    Plot Access Success Probability (P_S) vs M.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    # Keep UE sweep style consistent with Figure 3/4/5.
    ax.plot(data['M_values'], data['P_S_values'],
            'b-', linewidth=2, label='Simulation Curve')
    ax.plot(data['M_values'], data['P_S_values'],
            'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
            label='Simulation Results')

    ax.set_xlabel('M (Number of UEs)', fontsize=12)
    ax.set_ylabel('Access Success Probability ($P_S$)', fontsize=12, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax.set_ylim(0, 1.05)

    N = data.get('N', '?')
    I_max = data.get('I_max', '?')
    ax.set_title(f'UE Sweep: Access Success Probability vs M (N={N}, I_max={I_max})',
                 fontsize=13, fontweight='bold')

    ax.legend(loc='upper left', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Saved: {save_path}")

    if show:
        plt.show()

    return fig


def plot_ue_sweep_ta(data: dict, *, save_path: str = None, show: bool = False):
    """
    Plot Mean Access Delay (T_a) vs M.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data['M_values'], data['T_a_values'],
            'b-', linewidth=2, label='Simulation Curve')
    ax.plot(data['M_values'], data['T_a_values'],
            'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
            label='Simulation Results')

    ax.set_xlabel('M (Number of UEs)', fontsize=12)
    ax.set_ylabel('Mean Access Delay ($T_a$)', fontsize=12, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')

    N = data.get('N', '?')
    I_max = data.get('I_max', '?')
    ax.set_title(f'UE Sweep: Mean Access Delay vs M (N={N}, I_max={I_max})',
                 fontsize=13, fontweight='bold')

    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Saved: {save_path}")

    if show:
        plt.show()

    return fig


def plot_ue_sweep_pc(data: dict, *, save_path: str = None, show: bool = False):
    """
    Plot Collision Probability (P_C) vs M.
    """
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(data['M_values'], data['P_C_values'],
            'b-', linewidth=2, label='Simulation Curve')
    ax.plot(data['M_values'], data['P_C_values'],
            'bo', markersize=6, markerfacecolor='none', markeredgewidth=1.5,
            label='Simulation Results')

    ax.set_xlabel('M (Number of UEs)', fontsize=12)
    ax.set_ylabel('Collision Probability ($P_C$)', fontsize=12, color='blue')
    ax.tick_params(axis='y', labelcolor='blue')
    ax.set_ylim(0, 1.0)

    N = data.get('N', '?')
    I_max = data.get('I_max', '?')
    ax.set_title(f'UE Sweep: Collision Probability vs M (N={N}, I_max={I_max})',
                 fontsize=13, fontweight='bold')

    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    if save_path:
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"  Saved: {save_path}")

    if show:
        plt.show()

    return fig


def plot_ue_sweep_all(data: dict, *, save_dir: str = None, show: bool = False):
    """
    Plot all three UE sweep figures (P_S, T_a, P_C vs M).
    """
    save_ps = save_ta = save_pc = None
    if save_dir:
        save_dir = Path(save_dir)
        save_dir.mkdir(parents=True, exist_ok=True)
        save_ps = str(save_dir / "ue_sweep_ps.png")
        save_ta = str(save_dir / "ue_sweep_ta.png")
        save_pc = str(save_dir / "ue_sweep_pc.png")

    fig_ps = plot_ue_sweep_ps(data, save_path=save_ps, show=False)
    fig_ta = plot_ue_sweep_ta(data, save_path=save_ta, show=False)
    fig_pc = plot_ue_sweep_pc(data, save_path=save_pc, show=show)

    return fig_ps, fig_ta, fig_pc
