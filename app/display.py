"""Display and print helper functions for the CLI interface."""
from __future__ import annotations

from typing import NoReturn

from simulation.core.paths import relpath


def _exit_missing_dependency(e: ModuleNotFoundError, *, context: str) -> NoReturn:
    raise SystemExit(
        f"Missing Python dependency ({getattr(e, 'name', 'unknown')}), cannot run {context}.\n"
        f"Please run the following at the project root:\n"
        f"  - uv sync\n"
        f"Then run:\n"
        f"  - uv run python main.py ..."
    ) from e


def _print_output_path(path, *, label: str = "Output") -> None:
    if not path:
        return
    print(f"{label}: {relpath(path)}")


def _print_analytical_params(*, M: int, I_max: int, N_values, figure_name: str = ""):
    """Print analytical configuration summary matching FYP2 style."""
    print("------ Analytical Configuration ------")
    if figure_name:
        print(f"  [Figure]")
        print(f"  {figure_name}")
        print()
    print("  [Parameters]")
    print(f"  M={M}, I_max={I_max}")
    print()
    print("  [N Values]")
    print(f"  N = {list(N_values)}")
    print("--------------------------------------")
    print()


def _print_simulation_params(*, M: int, I_max: int, N_values, num_samples: int, num_workers: int = -1):
    """Print simulation configuration summary matching FYP2 style."""
    print("------ Simulation Configuration ------")
    print("  [Parameters]")
    print(f"  M={M}, I_max={I_max}")
    print()
    print("  [N Values]")
    print(f"  N = {list(N_values)}")
    print()
    print("  [Monte Carlo]")
    print(f"  num_samples = {num_samples:,}")
    if num_workers == -1:
        import os
        print(f"  num_workers = auto ({os.cpu_count()} cores)")
    else:
        print(f"  num_workers = {num_workers}")
    print("--------------------------------------")
    print()


def _confirm_run() -> bool:
    """Ask user to confirm before running. Returns True to proceed, False to cancel."""
    confirm = input("Ready to run? [Y/n] (Enter = Y): ").strip().lower()
    if confirm == "n":
        print("Cancelled.")
        return False
    return True
