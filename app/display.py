"""Display and print helper functions for the CLI interface."""
from __future__ import annotations

from typing import NoReturn

from simulation.core.paths import relpath


def format_n_values_for_display(values) -> str:
    """
    Compact CLI display for N sweeps: contiguous integers with step 1 as 'min-max',
    otherwise the same list form as before (e.g. [3, 14]).
    """
    if values is None:
        return ""
    seq = sorted(int(x) for x in values)
    if not seq:
        return str(list(seq))
    if len(seq) >= 2 and seq[-1] - seq[0] == len(seq) - 1:
        return f"{seq[0]}-{seq[-1]}"
    return str(list(seq))


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
        print("  [Figure]")
        print(f"  {figure_name}")
        print()
    print("  [UE]")
    print(f"  M={M}")
    print()
    print("  [Access Cycle]")
    print(f"  I_max={I_max}")
    print()
    print("  [RAO Slots]")
    print(f"  N={format_n_values_for_display(N_values)}")
    print("--------------------------------------")
    print()


def _print_simulation_params(*, M: int, I_max: int, N_values, num_samples: int):
    """Print simulation configuration summary matching FYP2 style."""
    print("------ Configuration ------")
    print("  [UE]")
    print(f"  M={M}")
    print()
    print("  [Access Cycle]")
    print(f"  I_max={I_max}")
    print()
    print("  [RAO Slots]")
    print(f"  N={format_n_values_for_display(N_values)}")
    print()
    print("  [Run]")
    print(f"  Samples={num_samples:,}")
    print("--------------------------------------")
    print()


def _confirm_run() -> bool:
    """Ask user to confirm before running. Returns True to proceed, False to cancel."""
    confirm = input("Ready to run? [Y/n] (Enter = Y): ").strip().lower()
    if confirm == "n":
        print("Cancelled.")
        return False
    return True
