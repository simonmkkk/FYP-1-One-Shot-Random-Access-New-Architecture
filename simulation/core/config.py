# ============================================================================
# config - Simulation configuration dataclass
# ============================================================================

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, List, Optional
from collections.abc import Mapping
from pathlib import Path

import yaml

from simulation.core.constants import (
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_I_MAX,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_NUM_WORKERS,
)


# ============================================================================
# Config dataclass
# ============================================================================

@dataclass
class Config:
    """
    Simulation configuration for One-Shot Random Access.

    Attributes:
        M: Number of UEs attempting access.
        N: Number of RAOs (Preamble pool size).
        I_max: Maximum Access Cycle count.
        num_samples: Monte Carlo sample count.
        num_workers: Parallel worker count (-1 = all CPU cores).
        n_values: N value list to sweep (for N-scan).
        m_values: M value list to sweep (for UE-scan).
        random_seed: Random seed for reproducibility (None = non-fixed).
        save_csv: Whether to save CSV output.
        result_dir: Output directory for results.
        experiment_name: Experiment name.
    """
    # Simulation parameters
    M: int = DEFAULT_M
    N: int = DEFAULT_N
    I_max: int = DEFAULT_I_MAX
    num_samples: int = DEFAULT_NUM_SAMPLES
    num_workers: int = DEFAULT_NUM_WORKERS

    # Sweep values
    n_values: Optional[List[int]] = None
    m_values: Optional[List[int]] = None

    # Control parameters
    random_seed: Optional[int] = None

    # Output parameters
    save_csv: bool = True
    result_dir: str = "result/simulation"
    experiment_name: str = "simulation"

    # ========================================================================
    # Computed properties
    # ========================================================================

    @property
    def n_range(self) -> List[int]:
        """Get N-value list."""
        if self.n_values is not None:
            return self.n_values
        return [self.N]

    @property
    def m_range(self) -> List[int]:
        """Get M-value list."""
        if self.m_values is not None:
            return self.m_values
        return [self.M]

    # ========================================================================
    # Config modification methods
    # ========================================================================

    def with_n(self, n: int) -> "Config":
        """Create a new Config with a different N value."""
        return Config(
            M=self.M, N=n, I_max=self.I_max,
            num_samples=self.num_samples, num_workers=self.num_workers,
            n_values=self.n_values, random_seed=self.random_seed,
            save_csv=self.save_csv, result_dir=self.result_dir,
            experiment_name=self.experiment_name,
        )

    def with_seed(self, seed: int) -> "Config":
        """Create a new Config with a different random seed."""
        return Config(
            M=self.M, N=self.N, I_max=self.I_max,
            num_samples=self.num_samples, num_workers=self.num_workers,
            n_values=self.n_values, random_seed=seed,
            save_csv=self.save_csv, result_dir=self.result_dir,
            experiment_name=self.experiment_name,
        )

    # ========================================================================
    # YAML loading
    # ========================================================================

    @staticmethod
    def parse_n_values(value) -> Optional[List[int]]:
        """
        Parse n_values from YAML into a list of integers.

        Supports:
            - range string: "10-300:10" → [10, 20, ..., 300]
            - range string: "5-45" → [5, 6, ..., 45]
            - comma string: "5,10,15" → [5, 10, 15]
            - list: [5, 10, 15] → [5, 10, 15]
            - int: 50 → [50]
            - None → None
        """
        if value is None:
            return None
        if isinstance(value, int):
            return [value]
        if isinstance(value, list):
            return sorted(int(v) for v in value)

        text = str(value).strip()

        # Range format: "start-end" or "start-end:step"
        if "-" in text and "," not in text:
            if ":" in text:
                range_part, step_str = text.rsplit(":", 1)
                step = int(step_str.strip())
            else:
                range_part = text
                step = 1
            parts = range_part.split("-")
            if len(parts) == 2:
                start, end = int(parts[0].strip()), int(parts[1].strip())
                return list(range(start, end + 1, step))

        # Comma-separated: "5,10,15"
        if "," in text:
            return sorted(int(v.strip()) for v in text.split(",") if v.strip())

        return [int(text)]

    @classmethod
    def from_yaml(cls, raw: Mapping[str, Any]) -> "Config":
        """Create Config from a YAML dictionary."""
        sim = raw.get("simulation", {})
        output = raw.get("output", {})
        exp = raw.get("experiment", {})

        # Sweep values (at top level or inside experiment)
        raw_n = raw.get("n_values", exp.get("n_values", None))
        n_values = cls.parse_n_values(raw_n)
        raw_m = raw.get("m_values", exp.get("m_values", None))
        m_values = cls.parse_n_values(raw_m)

        return cls(
            M=sim.get("M", DEFAULT_M),
            N=sim.get("N", DEFAULT_N),
            I_max=sim.get("I_max", DEFAULT_I_MAX),
            num_samples=sim.get("num_samples", DEFAULT_NUM_SAMPLES),
            num_workers=sim.get("num_workers", DEFAULT_NUM_WORKERS),
            n_values=n_values,
            m_values=m_values,
            random_seed=sim.get("random_seed", None),
            save_csv=output.get("save_csv", True),
            result_dir=output.get("result_dir", "result/simulation"),
            experiment_name=exp.get("name", "simulation"),
        )

    @classmethod
    def from_yaml_file(cls, path: Path | str) -> "Config":
        """Create Config from a YAML file."""
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        return cls.from_yaml(raw)


__all__ = [
    "Config",
]
