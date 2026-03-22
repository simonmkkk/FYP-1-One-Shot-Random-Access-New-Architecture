# ============================================================================
# Simulation: UE Sweep — P_S, T_a, P_C vs M (fixed N)
# ============================================================================

from pathlib import Path
from typing import List

from simulation.core.runner import run_experiment
from simulation.core.metrics import SimulationResult


def run_ue_sweep() -> List[SimulationResult]:
    """
    Run UE sweep simulation — M value sweep with fixed N.

    Returns:
        List[SimulationResult]: Simulation results list.
    """
    PROJECT_ROOT = Path(__file__).resolve().parent.parent
    config_path = PROJECT_ROOT / "configs" / "simulation" / "config_ue_sweep.yaml"
    return run_experiment(config_path)


if __name__ == "__main__":
    run_ue_sweep()
