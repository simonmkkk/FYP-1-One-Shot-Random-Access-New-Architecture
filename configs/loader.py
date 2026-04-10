# ============================================================================
# Config loader - Read and parse YAML configuration files
# ============================================================================

import yaml
from pathlib import Path
from typing import Any, Dict


# Configs root directory (this file's parent)
CONFIGS_ROOT = Path(__file__).resolve().parent


def get_config_path(config_type: str, config_name: str) -> Path:
    """
    Get the full path to a config file.

    Args:
        config_type: Config category ('analytical' or 'simulation').
        config_name: Config file name (without .yaml extension).

    Returns:
        Absolute path to the YAML file.
    """
    if not config_name.startswith("config_"):
        config_name = f"config_{config_name}"
    if not config_name.endswith('.yaml') and not config_name.endswith('.yml'):
        config_name = f"{config_name}.yaml"

    return CONFIGS_ROOT / config_type / config_name


def load_config(config_type: str, config_name: str) -> Dict[str, Any]:
    """
    Load a YAML configuration file.

    Args:
        config_type: Config category ('analytical' or 'simulation').
        config_name: Config file name (without .yaml extension).

    Returns:
        Configuration dictionary.
    """
    config_path = get_config_path(config_type, config_name)

    if not config_path.exists():
        available = list_available_configs(config_type)
        raise FileNotFoundError(
            f"Config file not found: {config_path}\n"
            f"Available configs: {available}"
        )

    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)

    return config


def list_available_configs(config_type: str = None) -> dict:
    """
    List all available configuration files.

    Args:
        config_type: Config category (None = list all).

    Returns:
        Dictionary of config names by category.
    """
    configs = {}

    types = [config_type] if config_type else ['analytical', 'simulation']

    for ctype in types:
        type_dir = CONFIGS_ROOT / ctype
        if type_dir.exists():
            configs[ctype] = []
            for file in type_dir.glob('*.yaml'):
                configs[ctype].append(file.stem)
            for file in type_dir.glob('*.yml'):
                configs[ctype].append(file.stem)

    return configs
