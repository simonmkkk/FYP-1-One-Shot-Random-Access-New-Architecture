# ============================================================================
# Configs Module - Simple YAML configuration loading
# ============================================================================
"""Simple configuration loading from YAML files.

Usage:
    from configs import load_config
    config = load_config("analytical", "figure1")
    print(config["n_values"])  # → [3, 14]
"""

from .loader import load_config, get_config_path, list_available_configs

__all__ = [
    "load_config",
    "get_config_path",
    "list_available_configs",
]
