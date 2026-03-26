# ============================================================================
# paths - Central result-path helpers shared by simulation and app layers
#
# ALL outputs go under result/runs/<category>/<run_name>_<timestamp>/.
#   category = analytical | simulation | plot | pipeline
#
# No "latest" directory — all data is accessed via explicit run directories.
# ============================================================================

from __future__ import annotations

import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Dict


def project_root() -> Path:
    """
    Return the repository root.
    """
    current = Path(__file__).resolve().parent
    for parent in [current, *current.parents]:
        if (parent / "pyproject.toml").is_file():
            return parent
    return current


def timestamp_string() -> str:
    """
    Return a filesystem-safe timestamp.
    """
    return datetime.now().strftime("%Y%m%d_%H%M%S")


PROJECT_ROOT = project_root()
RESULT_ROOT = PROJECT_ROOT / "result"
RUNS_ROOT = RESULT_ROOT / "runs"

# Category roots under result/runs/
ANALYTICAL_ROOT = RUNS_ROOT / "analytical"
SIMULATION_ROOT = RUNS_ROOT / "simulation"
PLOT_ROOT = RUNS_ROOT / "plot"
PIPELINE_ROOT = RUNS_ROOT / "pipeline"


# ============================================================================
# Run layout helpers — flat structure
# ============================================================================
def ensure_run_dir(run_dir: Path) -> Path:
    """
    Create the run directory and return it.

    CSVs, graphs, and metadata.json all live directly inside
    the run directory (no sub-nesting).
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


# ============================================================================
# Run directory creators — standalone operations
# ============================================================================
def create_analytical_run_dir(name: str = "") -> Path:
    """Return the flat analytical output directory (no timestamps).

    All analytical CSVs live directly in ANALYTICAL_ROOT and are
    overwritten on every run.
    """
    ANALYTICAL_ROOT.mkdir(parents=True, exist_ok=True)
    return ANALYTICAL_ROOT


def create_simulation_run_dir(name: str) -> Path:
    """Create a timestamped run dir under the simulation project directory.

    Layout: result/runs/simulation/<name>/<timestamp>/
    """
    return ensure_run_dir(SIMULATION_ROOT / name / timestamp_string())


def create_plot_run_dir(name: str) -> Path:
    """Create a timestamped run dir for a standalone plot operation."""
    return ensure_run_dir(PLOT_ROOT / f"{timestamp_string()}_{name}")


def create_pipeline_run_dir(name: str) -> Path:
    """Create a timestamped run dir for a pipeline operation."""
    return ensure_run_dir(PIPELINE_ROOT / f"{timestamp_string()}_{name}")


def create_plot_all_run_dir() -> Path:
    """Create a timestamped run dir for 'Plot All'."""
    return ensure_run_dir(PLOT_ROOT / f"{timestamp_string()}_all")


# ============================================================================
# Metadata helpers
# ============================================================================
def write_metadata(run_dir: Path, payload: Dict[str, Any]) -> Path:
    """
    Write a metadata.json file in the given directory.
    """
    run_dir = Path(run_dir)
    run_dir.mkdir(parents=True, exist_ok=True)
    target = run_dir / "metadata.json"
    if "timestamp" not in payload:
        payload["timestamp"] = datetime.now().isoformat()
    target.write_text(json.dumps(payload, indent=2, sort_keys=False, default=str), encoding="utf-8")
    return target


# ============================================================================
# Data source copy helper (for plot runs)
# ============================================================================
def copy_data_source(
    src: Path,
    dest_dir: Path,
    category: str,
) -> Path:
    """
    Copy a source CSV into a plot's data/ subfolder.

    Naming convention: copy_of_<category>__<original_filename>
    e.g. copy_of_analytical__figure345.csv

    Args:
        src:       absolute path to the source CSV
        dest_dir:  the plot run directory (data/ will be created inside it)
        category:  'analytical' or 'simulation'

    Returns:
        The path to the copied file.
    """
    data_dir = Path(dest_dir) / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    dest_name = f"copy_of_{category}__{src.name}"
    dest = data_dir / dest_name
    shutil.copy2(str(src), str(dest))
    return dest


# ============================================================================
# Utility helpers
# ============================================================================
def relpath(path: str | Path) -> Path:
    """
    Return a project-relative path when possible.
    """
    p = Path(path)
    try:
        return p.relative_to(PROJECT_ROOT)
    except ValueError:
        return p


__all__ = [
    "PROJECT_ROOT",
    "RESULT_ROOT",
    "RUNS_ROOT",
    "ANALYTICAL_ROOT",
    "SIMULATION_ROOT",
    "PLOT_ROOT",
    "PIPELINE_ROOT",
    "ensure_run_dir",
    "create_analytical_run_dir",
    "create_simulation_run_dir",
    "create_plot_run_dir",
    "create_pipeline_run_dir",
    "create_plot_all_run_dir",
    "write_metadata",
    "copy_data_source",
    "relpath",
    "timestamp_string",
]
