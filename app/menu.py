#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ============================================================================
# Menu - Interactive menu for the simulation & analysis system
# ============================================================================

import os
import sys
import select
import time

from .commands import (
    run_analytical_figure1,
    run_analytical_figure2,
    run_analytical_figure345,
    run_analytical_all,
    run_simulation_figure345,
    run_simulation_ue_sweep,
    run_plot_figure1,
    run_plot_figure2,
    run_plot_figure345,
    run_plot_ue_sweep,
    run_plot_all,
    run_pipeline_figure1,
    run_pipeline_figure2,
    run_pipeline_figure345,
    run_pipeline_ue_sweep,
    run_pipeline_all,
)


def _clear_screen() -> None:
    """
    Clear the terminal screen for a clean view.
    """
    os.system("cls" if os.name == "nt" else "clear")


def _wait_for_fresh_enter(prompt: str) -> None:
    """
    Wait for a *new* Enter key press.

    Any key presses that happened while a long-running action was executing
    are drained first, so they won't accidentally skip this pause.
    """
    # Drain any pending input without blocking
    try:
        while select.select([sys.stdin], [], [], 0)[0]:
            sys.stdin.readline()
    except (OSError, ValueError):
        # If stdin is not selectable (e.g. redirected), fall back to normal input
        pass

    # Now wait for a fresh Enter
    input(prompt)


# ============================================================================
# Menu Configuration - Dict-based dispatch
# ============================================================================
MENU_ACTIONS = {
    "1": run_analytical_figure1,
    "2": run_analytical_figure2,
    "3": run_analytical_figure345,
    "4": run_analytical_all,

    "5": run_simulation_figure345,
    "6": run_simulation_ue_sweep,

    "7": run_plot_figure1,
    "8": run_plot_figure2,
    "9": run_plot_figure345,
    "10": run_plot_ue_sweep,
    "11": run_plot_all,

    "12": run_pipeline_figure1,
    "13": run_pipeline_figure2,
    "14": run_pipeline_figure345,
    "15": run_pipeline_ue_sweep,
    "16": run_pipeline_all,
}

# Category and label (without number) for menu, used when running an item
MENU_CATEGORIES = {
    "1": "Analytical",
    "2": "Analytical",
    "3": "Analytical",
    "4": "Analytical",
    "5": "Simulation",
    "6": "Simulation",
    "7": "Plot",
    "8": "Plot",
    "9": "Plot",
    "10": "Plot",
    "11": "Plot",
    "12": "Pipeline",
    "13": "Pipeline",
    "14": "Pipeline",
    "15": "Pipeline",
    "16": "Pipeline",
}

MENU_LABELS = {
    "1": "Figure 1: NS,1/N & NC,1/N exact + approximate",
    "2": "Figure 2: Approximation Error (exact vs approximate)",
    "3": "Figure 3, 4, 5 combined analysis (P_S, T_a, P_C)",
    "4": "Run all analytical calculations",
    "5": "Figure 3, 4, 5 combined simulation (P_S, T_a, P_C)",
    "6": "UE Sweep simulation (P_S, T_a, P_C vs M, fixed N)",
    "7": "Plot Figure 1",
    "8": "Plot Figure 2",
    "9": "Plot Figure 3, 4, 5",
    "10": "Plot UE Sweep (P_S, T_a, P_C vs M)",
    "11": "Plot all figures",
    "12": "Figure 1 full pipeline (Analytical + Plot)",
    "13": "Figure 2 full pipeline (Analytical + Plot)",
    "14": "Figure 3, 4, 5 full pipeline (Analytical + Simulation + Plot)",
    "15": "UE Sweep full pipeline (Simulation + Plot)",
    "16": "All figures full pipeline",
}


# ============================================================================
# Menu Display
# ============================================================================
def print_menu():
    """
    Print the interactive menu.

    Shows all analysis options.
    """
    print("One-Shot Random Access - Simulation & Analysis System")
    print()
    print("Please select an option:\n")

    # Analytical options
    print("[Analytical]")
    print("   1. Figure 1: NS,1/N & NC,1/N exact + approximate")
    print("   2. Figure 2: Approximation Error (exact vs approximate)")
    print("   3. Figure 3, 4, 5 combined analysis (P_S, T_a, P_C)")
    print("   4. Run all analytical calculations")

    # Simulation options
    print("\n[Simulation]")
    print("   5. Figure 3, 4, 5 combined simulation (P_S, T_a, P_C)")
    print("   6. UE Sweep simulation (P_S, T_a, P_C vs M, fixed N)")

    # Plot options
    print("\n[Plot]")
    print("   7. Plot Figure 1")
    print("   8. Plot Figure 2")
    print("   9. Plot Figure 3, 4, 5")
    print("  10. Plot UE Sweep (P_S, T_a, P_C vs M)")
    print("  11. Plot all figures")

    # Pipeline options (Analytical + Sim + Plot)
    print("\n[Pipeline] (Analytical + Simulation + Plot)")
    print("  12. Figure 1 full pipeline (Analytical + Plot)")
    print("  13. Figure 2 full pipeline (Analytical + Plot)")
    print("  14. Figure 3, 4, 5 full pipeline (Analytical + Simulation + Plot)")
    print("  15. UE Sweep full pipeline (Simulation + Plot)")
    print("  16. All figures full pipeline")

    print("\n   0. Exit")


def show_menu():
    """
    Main menu loop.
    """
    while True:
        _clear_screen()
        print_menu()

        try:
            choice = input("\nEnter your choice: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if choice == "0":
            print("\nGoodbye!")
            break

        action = MENU_ACTIONS.get(choice)
        if action:
            category = MENU_CATEGORIES.get(choice)
            label = MENU_LABELS.get(choice)

            # Clear the menu and show only the choice + run info.
            _clear_screen()

            # Keep the title visible above the output.
            print("One-Shot Random Access - Simulation & Analysis System")
            if category and label:
                print()
                print(f"Enter your choice: {choice}")
                print()
                print(f"[{category}]")
                print(f"   {choice}. {label}")

            # Run the selected action and keep all output on screen.
            result = action()
            try:
                # If the action explicitly returns False, treat it as "cancel/back"
                # and return to the menu immediately (no pause).
                if result is False:
                    continue
                _wait_for_fresh_enter("\nPress Enter to return to menu...")
            except (KeyboardInterrupt, EOFError):
                break
        else:
            print("\nInvalid choice, please try again")
            time.sleep(1.5)


# ============================================================================
# Interactive Menu - Main Entry Point
# ============================================================================
def interactive_menu():
    """
    Interactive menu main loop.

    Runs until the user chooses to exit.
    """
    show_menu()
