# ============================================================================
# metrics - Performance metrics computation
# ============================================================================
#
# Computes statistical metrics and confidence intervals from simulation results.
#
# Provides:
# 1. SimulationResult — dataclass for structured simulation output
# 2. confidence_interval_95() — 95% confidence interval (half-width)
# 3. calculate_performance_metrics() — mean and CI computation
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


# ============================================================================
# Simulation result dataclass
# ============================================================================

@dataclass
class SimulationResult:
    """
    Simulation result for a single N value.

    Attributes:
        N: Number of RAOs (Preamble pool size).
        M: Number of UEs attempting access.
        I_max: Maximum Access Cycle count.
        num_samples: Number of simulation samples.
        mean_ps: Mean Access Success Probability (P_S), range [0, 1].
        mean_ta: Mean Access Delay (T_a), in AC units.
        mean_pc: Mean Collision Probability (P_C), range [0, 1].
        ci_ps: P_S 95% confidence interval (half-width).
        ci_ta: T_a 95% confidence interval (half-width).
        ci_pc: P_C 95% confidence interval (half-width).
    """
    N: int
    M: int
    I_max: int
    num_samples: int
    mean_ps: float = 0.0
    mean_ta: float = 0.0
    mean_pc: float = 0.0
    ci_ps: float = 0.0
    ci_ta: float = 0.0
    ci_pc: float = 0.0


# ============================================================================
# Statistical functions
# ============================================================================

def confidence_interval_95(data: np.ndarray) -> float:
    """
    Compute 95% confidence interval (half-width).

    Formula: CI = z * (sigma / sqrt(n)), where z = 1.96.

    Args:
        data: Sample data array.

    Returns:
        float: 95% confidence interval half-width.
    """
    if len(data) == 0:
        return 0.0
    return 1.96 * np.std(data) / np.sqrt(len(data))


def calculate_performance_metrics(
    results_array: np.ndarray,
) -> Tuple[Tuple[float, float, float], Tuple[float, float, float]]:
    """
    Compute mean performance metrics from simulation results.

    Metrics:
    1. P_S (Access Success Probability)
    2. T_a (Mean Access Delay) — only valid samples (delay >= 0)
    3. P_C (Collision Probability)

    Args:
        results_array: Shape [num_samples, 3].
            Column 0: P_S, Column 1: T_a, Column 2: P_C.

    Returns:
        tuple: ((mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc)).
    """
    # P_S mean
    mean_ps = np.mean(results_array[:, 0])

    # P_C mean
    mean_pc = np.mean(results_array[:, 2])

    # T_a mean (filter valid: delay >= 0, since -1 = no successful access)
    valid_ta_samples = results_array[results_array[:, 1] >= 0, 1]
    if len(valid_ta_samples) > 0:
        mean_ta = np.mean(valid_ta_samples)
        ci_ta = confidence_interval_95(valid_ta_samples)
    else:
        mean_ta = 0
        ci_ta = 0

    # Confidence intervals
    ci_ps = confidence_interval_95(results_array[:, 0])
    ci_pc = confidence_interval_95(results_array[:, 2])

    return (mean_ps, mean_ta, mean_pc), (ci_ps, ci_ta, ci_pc)


# ============================================================================
# Module exports
# ============================================================================

__all__ = [
    "SimulationResult",
    "confidence_interval_95",
    "calculate_performance_metrics",
]
