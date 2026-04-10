# ============================================================================
# runner - Parallel execution and experiment management
# ============================================================================

from __future__ import annotations

import csv
import gc
from pathlib import Path
from typing import List, Optional, Sequence

from simulation.core.config import Config
from simulation.core.metrics import SimulationResult, calculate_performance_metrics
from simulation.core.one_shot_access import simulate_group_paging_multi_samples
from simulation.core.paths import (
    create_simulation_run_dir,
    relpath,
    write_metadata,
)


# ============================================================================
# Single-point simulation
# ============================================================================

def run_single_n_simulation(cfg: Config, n_value: int) -> SimulationResult:
    """
    Run simulation for a single N value.

    Args:
        cfg: Simulation configuration.
        n_value: N value (RAO count).

    Returns:
        SimulationResult with P_S, T_a, P_C means and confidence intervals.
    """
    results_array = simulate_group_paging_multi_samples(
        M=cfg.M,
        N=n_value,
        I_max=cfg.I_max,
        num_samples=cfg.num_samples,
        num_workers=cfg.num_workers,
    )

    means, cis = calculate_performance_metrics(results_array)
    mean_ps, mean_ta, mean_pc = means
    ci_ps, ci_ta, ci_pc = cis

    del results_array
    gc.collect()

    return SimulationResult(
        N=n_value,
        M=cfg.M,
        I_max=cfg.I_max,
        num_samples=cfg.num_samples,
        mean_ps=mean_ps,
        mean_ta=mean_ta,
        mean_pc=mean_pc,
        ci_ps=ci_ps,
        ci_ta=ci_ta,
        ci_pc=ci_pc,
    )


# ============================================================================
# N-value sweep
# ============================================================================

def run_n_scan(
    cfg: Config,
    n_values: Sequence[int] | None = None,
) -> List[SimulationResult]:
    """
    Run N-value sweep simulation.

    Args:
        cfg: Base simulation configuration.
        n_values: N values to sweep (None = use cfg.n_range).

    Returns:
        List[SimulationResult] for each N value.
    """
    if n_values is None:
        n_values = cfg.n_range

    results: List[SimulationResult] = []

    for n in n_values:
        result = run_single_n_simulation(cfg, n)
        results.append(result)
        print(f"  N={n}: P_S={result.mean_ps:.6f}, T_a={result.mean_ta:.4f}, P_C={result.mean_pc:.6f}")

    return results


# ============================================================================
# M-value sweep (UE count sweep, fixed N)
# ============================================================================

def run_m_scan(
    cfg: Config,
    m_values: Sequence[int] | None = None,
) -> List[SimulationResult]:
    """
    Run M-value (UE count) sweep simulation with fixed N.

    Args:
        cfg: Base simulation configuration.
        m_values: M values to sweep (None = use cfg.m_range).

    Returns:
        List[SimulationResult] for each M value.
    """
    if m_values is None:
        m_values = cfg.m_range

    results: List[SimulationResult] = []

    for m in m_values:
        results_array = simulate_group_paging_multi_samples(
            M=m,
            N=cfg.N,
            I_max=cfg.I_max,
            num_samples=cfg.num_samples,
            num_workers=cfg.num_workers,
        )

        means, cis = calculate_performance_metrics(results_array)
        mean_ps, mean_ta, mean_pc = means
        ci_ps, ci_ta, ci_pc = cis

        del results_array
        gc.collect()

        result = SimulationResult(
            N=cfg.N,
            M=m,
            I_max=cfg.I_max,
            num_samples=cfg.num_samples,
            mean_ps=mean_ps,
            mean_ta=mean_ta,
            mean_pc=mean_pc,
            ci_ps=ci_ps,
            ci_ta=ci_ta,
            ci_pc=ci_pc,
        )
        results.append(result)
        print(f"  M={m}: P_S={result.mean_ps:.6f}, T_a={result.mean_ta:.4f}, P_C={result.mean_pc:.6f}")

    return results


# ============================================================================
# CSV output
# ============================================================================

CSV_FIELDNAMES = [
    "N", "M", "I_max",
    "P_S", "T_a", "P_C",
    "CI_P_S", "CI_T_a", "CI_P_C",
    "num_samples",
]


def save_results_to_csv(
    results: List[SimulationResult],
    output_path: Path,
) -> None:
    """Save simulation results to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDNAMES)
        writer.writeheader()

        for result in results:
            writer.writerow({
                "N": result.N,
                "M": result.M,
                "I_max": result.I_max,
                "P_S": result.mean_ps,
                "T_a": result.mean_ta,
                "P_C": result.mean_pc,
                "CI_P_S": result.ci_ps,
                "CI_T_a": result.ci_ta,
                "CI_P_C": result.ci_pc,
                "num_samples": result.num_samples,
            })

    print(f"  Output: {relpath(output_path)}")


# ============================================================================
# Unified experiment entry
# ============================================================================

def run_experiment(
    config_path: Path | str,
    output_dir: Optional[Path] = None,
) -> List[SimulationResult]:
    """
    Unified experiment runner.

    Auto-detects sweep type:
    - If m_values is set → M-sweep (UE count sweep, fixed N)
    - Otherwise → N-sweep (RAO sweep, fixed M)

    Args:
        config_path: Path to YAML configuration file.
        output_dir: If set, save CSV to this directory.
                    Otherwise use timestamped path under result/runs/simulation/.

    Returns:
        List[SimulationResult].
    """
    config_path = Path(config_path)
    cfg = Config.from_yaml_file(config_path)

    # Auto-detect sweep type
    if cfg.m_values is not None:
        results = run_m_scan(cfg)
    else:
        results = run_n_scan(cfg)

    if cfg.save_csv:
        if output_dir is None:
            output_dir = create_simulation_run_dir(cfg.experiment_name)
        else:
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

        output_path = output_dir / f"{cfg.experiment_name}.csv"
        save_results_to_csv(results, output_path)

        write_metadata(output_dir, {
            "title": f"Simulation: {cfg.experiment_name}",
            "run_type": "simulation",
            "config": cfg.experiment_name,
            "produced_files": {
                "csv": output_path.name,
            },
        })

    return results


__all__ = [
    "run_single_n_simulation",
    "run_n_scan",
    "run_m_scan",
    "save_results_to_csv",
    "CSV_FIELDNAMES",
    "run_experiment",
]

