"""
配置管理模組

加載和管理 YAML 配置文件。

Input: config/ 目錄下的 YAML 配置文件
Output: load_config(), get_config_path(), list_available_configs()
Position: 系統配置的統一入口

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
"""

from .loader.loader import load_config, get_config_path, list_available_configs

__all__ = ['load_config', 'get_config_path', 'list_available_configs']

