"""
============================================================================
config - 模擬配置類
============================================================================

此模組定義 Config 配置類，使用 @dataclass 簡化配置管理。
參考 FYP-2 的架構設計。

Input: YAML 配置（dict/檔案）、模擬參數（M/N/I_max 等）、預設值
Output: `Config` 物件（供 simulator/runner 使用）
Position: simulation core 的配置層（所有模組共用的參數來源）

注意：一旦此文件被更新，請同步更新：
- 項目根目錄 README.md
============================================================================
"""

# ============================================================================
# 標準庫導入
# ============================================================================
from __future__ import annotations  # 啟用延遲類型註解評估

from dataclasses import dataclass  # dataclass 裝飾器，簡化類別定義
from typing import Any, List, Optional  # 類型提示工具
from collections.abc import Mapping  # 映射抽象基類，用於類型檢查
from pathlib import Path  # 物件導向的路徑處理

import yaml  # YAML 文件解析庫，用於載入配置文件

# ============================================================================
# 本地模組導入
# ============================================================================
from simulation.core.constants import (
    DEFAULT_M,
    DEFAULT_N,
    DEFAULT_I_MAX,
    DEFAULT_NUM_SAMPLES,
    DEFAULT_NUM_WORKERS,
    DEFAULT_N_SCAN_START,
    DEFAULT_N_SCAN_STOP,
    DEFAULT_N_SCAN_STEP,
)


# ============================================================================
# 配置類
# ============================================================================

@dataclass
class Config:
    """
    模擬配置類 - 使用 dataclass 管理 One-Shot Random Access 模擬參數
    
    所有參數都有合理的默認值，可以直接創建實例使用。
    提供便捷方法來創建具有不同參數的新配置實例。
    
    Attributes:
        M: 初始設備數量（嘗試接入的 UE 數）
        N: RAO 數量（Preamble pool size）
        I_max: 最大 Access Cycle 數
        num_samples: 模擬樣本數
        num_workers: 並行工作進程數（-1 表示使用所有 CPU 核心）
        n_scan_start: N 值掃描起始值
        n_scan_stop: N 值掃描結束值（不包含）
        n_scan_step: N 值掃描步長
        n_values: 自定義 N 值列表（優先於 scan range）
        random_seed: 隨機數種子，確保模擬結果可重現
        save_csv: 是否保存 CSV 結果
        result_dir: 結果保存目錄
        experiment_name: 實驗名稱
    """
    # ---- 模擬參數 ----
    M: int = DEFAULT_M                      # 初始設備數量
    N: int = DEFAULT_N                      # RAO 數量
    I_max: int = DEFAULT_I_MAX              # 最大 Access Cycle 數
    num_samples: int = DEFAULT_NUM_SAMPLES  # 模擬樣本數
    num_workers: int = DEFAULT_NUM_WORKERS  # 並行工作進程數
    
    # ---- N 值掃描配置 ----
    n_scan_start: int = DEFAULT_N_SCAN_START  # N 值掃描起始值
    n_scan_stop: int = DEFAULT_N_SCAN_STOP    # N 值掃描結束值
    n_scan_step: int = DEFAULT_N_SCAN_STEP    # N 值掃描步長
    n_values: Optional[List[int]] = None      # 自定義 N 值列表
    
    # ---- 控制參數 ----
    random_seed: Optional[int] = None         # 隨機種子（None 表示不固定）
    
    # ---- 輸出參數 ----
    save_csv: bool = True                     # 是否保存 CSV
    result_dir: str = "result/simulation"     # 結果目錄
    experiment_name: str = "simulation"       # 實驗名稱
    
    # ========================================================================
    # 計算屬性
    # ========================================================================
    
    @property
    def n_range(self) -> List[int]:
        """
        獲取 N 值掃描範圍
        
        如果指定了 n_values，使用之；否則根據 scan range 生成
        
        Returns:
            List[int]: N 值列表
        """
        if self.n_values is not None:
            return self.n_values
        return list(range(self.n_scan_start, self.n_scan_stop, self.n_scan_step))
    
    # ========================================================================
    # 配置修改方法
    # ========================================================================
    
    def with_n(self, n: int) -> "Config":
        """
        創建具有不同 N 值的新配置實例
        
        用於 N 掃描時動態修改 N 值
        
        Args:
            n: 新的 N 值
            
        Returns:
            Config: 新的配置實例
        """
        return Config(
            M=self.M,
            N=n,  # 使用新的 N 值
            I_max=self.I_max,
            num_samples=self.num_samples,
            num_workers=self.num_workers,
            n_scan_start=self.n_scan_start,
            n_scan_stop=self.n_scan_stop,
            n_scan_step=self.n_scan_step,
            n_values=self.n_values,
            random_seed=self.random_seed,
            save_csv=self.save_csv,
            result_dir=self.result_dir,
            experiment_name=self.experiment_name,
        )
    
    def with_seed(self, seed: int) -> "Config":
        """
        創建具有不同隨機種子的新配置實例
        
        用於多次運行時確保每次運行的隨機序列不同
        
        Args:
            seed: 新的隨機種子
            
        Returns:
            Config: 新的配置實例
        """
        return Config(
            M=self.M,
            N=self.N,
            I_max=self.I_max,
            num_samples=self.num_samples,
            num_workers=self.num_workers,
            n_scan_start=self.n_scan_start,
            n_scan_stop=self.n_scan_stop,
            n_scan_step=self.n_scan_step,
            n_values=self.n_values,
            random_seed=seed,  # 使用新的隨機種子
            save_csv=self.save_csv,
            result_dir=self.result_dir,
            experiment_name=self.experiment_name,
        )
    
    # ========================================================================
    # 從 YAML 載入
    # ========================================================================
    
    @classmethod
    def from_yaml(cls, raw: Mapping[str, Any]) -> "Config":
        """
        從 YAML 字典創建配置實例
        
        Args:
            raw: 從 YAML 文件載入的字典
            
        Returns:
            Config: 新的配置實例
        """
        # 提取各配置區塊，如果不存在則使用空字典
        sim = raw.get("simulation", {})
        scan = raw.get("scan", {}).get("range", {})
        output = raw.get("output", {})
        exp = raw.get("experiment", {})
        
        # 獲取自定義 n_values（如果有）
        n_values = exp.get("n_values", None)
        
        return cls(
            M=sim.get("M", DEFAULT_M),
            N=sim.get("N", DEFAULT_N),
            I_max=sim.get("I_max", DEFAULT_I_MAX),
            num_samples=sim.get("num_samples", DEFAULT_NUM_SAMPLES),
            num_workers=sim.get("num_workers", DEFAULT_NUM_WORKERS),
            n_scan_start=scan.get("start", DEFAULT_N_SCAN_START),
            n_scan_stop=scan.get("stop", DEFAULT_N_SCAN_STOP),
            n_scan_step=scan.get("step", DEFAULT_N_SCAN_STEP),
            n_values=n_values,
            random_seed=sim.get("random_seed", None),
            save_csv=output.get("save_csv", True),
            result_dir=output.get("result_dir", "result/simulation"),
            experiment_name=exp.get("name", "simulation"),
        )
    
    @classmethod
    def from_yaml_file(cls, path: Path | str) -> "Config":
        """
        從 YAML 文件創建配置實例
        
        Args:
            path: YAML 文件路徑
            
        Returns:
            Config: 新的配置實例
        """
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        return cls.from_yaml(raw)


# ============================================================================
# 模組導出
# ============================================================================

__all__ = [
    "Config",
]
