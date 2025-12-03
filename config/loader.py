"""
配置加載器模組
"""

import os
import yaml
from pathlib import Path
from typing import Any, Dict, Optional


def get_config_dir() -> Path:
    """獲取配置文件目錄的絕對路徑"""
    return Path(__file__).parent


def get_config_path(config_type: str, config_name: str) -> Path:
    """
    獲取指定配置文件的完整路徑
    
    Args:
        config_type: 配置類型 ('analytical' 或 'simulation')
        config_name: 配置文件名（不含 .yaml 後綴）
    
    Returns:
        配置文件的絕對路徑
    """
    config_dir = get_config_dir()
    
    if not config_name.endswith('.yaml') and not config_name.endswith('.yml'):
        config_name = f"{config_name}.yaml"
    
    return config_dir / config_type / config_name


def load_config(config_type: str, config_name: str) -> Dict[str, Any]:
    """
    從 YAML 文件加載配置
    
    Args:
        config_type: 配置類型 ('analytical' 或 'simulation')
        config_name: 配置文件名（不含 .yaml 後綴）
    
    Returns:
        配置字典
    """
    config_path = get_config_path(config_type, config_name)
    
    if not config_path.exists():
        raise FileNotFoundError(
            f"配置文件不存在: {config_path}\n"
            f"可用的配置文件: {list_available_configs(config_type)}"
        )
    
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    return config


def list_available_configs(config_type: str = None) -> dict:
    """
    列出所有可用的配置文件
    
    Args:
        config_type: 配置類型，None 表示列出所有
    
    Returns:
        配置文件字典
    """
    config_dir = get_config_dir()
    configs = {}
    
    types = [config_type] if config_type else ['analytical', 'simulation']
    
    for ctype in types:
        type_dir = config_dir / ctype
        if type_dir.exists():
            configs[ctype] = []
            for file in type_dir.glob('*.yaml'):
                configs[ctype].append(file.stem)
            for file in type_dir.glob('*.yml'):
                configs[ctype].append(file.stem)
    
    return configs


def save_config(config: Dict[str, Any], config_type: str, config_name: str) -> Path:
    """
    將配置保存到 YAML 文件
    """
    config_path = get_config_path(config_type, config_name)
    config_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, 'w', encoding='utf-8') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    return config_path

