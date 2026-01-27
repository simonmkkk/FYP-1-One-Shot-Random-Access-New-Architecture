# 配置文件詳解

本文檔詳細說明所有 YAML 配置文件的參數和用法。

---

## 配置文件總覽

| 配置文件                    | 用途              | 位置                 |
| --------------------------- | ----------------- | -------------------- |
| `figure1.yaml`              | Figure 1 & 2 解析 | `config/analytical/` |
| `figure345.yaml`            | Figure 3-5 解析   | `config/analytical/` |
| `simulation_figure345.yaml` | Figure 3-5 模擬   | `simulation/config/` |

---

## figure1.yaml (Figure 1 & 2 共用)

**路徑**: `config/analytical/figure1.yaml`

```yaml
# N 值列表 - 論文使用 N=3 和 N=14
n_values: [3, 14]

# M/N 最大值 - 論文範圍 0 到 10
m_over_n_max: 10

# M 起始值 - 論文從 M=1 開始
m_start: 1

# 並行計算核心數
# -1: 使用所有 CPU 核心
# 正整數: 指定核心數
n_jobs: -1
```

### 參數影響

| 參數           | 影響                                              |
| -------------- | ------------------------------------------------- |
| `n_values`     | 決定生成幾組數據（每個 N 一個 CSV）               |
| `m_over_n_max` | 決定 M 的範圍（M 從 m_start 到 m_over_n_max × N） |
| `n_jobs`       | 影響計算速度                                      |

---

## figure345.yaml (解析配置)

**路徑**: `config/analytical/figure345.yaml`

```yaml
# 設備總數 - 論文使用 M=100
M: 100

# 最大接入周期數 - 論文使用 I_max=10
I_max: 10

# N 範圍設定 - 論文範圍 5 到 45
N_start: 5    # N 起始值
N_stop: 46    # N 結束值（不包含）
N_step: 1     # N 步長
```

### 參數影響

| 參數    | 影響                     |
| ------- | ------------------------ |
| `M`     | 設備總數，影響系統負載   |
| `I_max` | 最大重試次數，影響成功率 |
| `N_*`   | 決定計算的 N 值範圍      |

---

## simulation_figure345.yaml (模擬配置)

**路徑**: `simulation/config/simulation_figure345.yaml`

```yaml
description: "Figure 3, 4, 5: Combined Simulation"

simulation:
  M: 100           # 設備總數
  I_max: 10        # 最大周期數

scan:
  parameter: N     # 掃描參數
  range:
    start: 5       # N 起始
    stop: 46       # N 結束
    step: 1        # N 步長

performance:
  num_samples: 10000000   # 樣本數 (10^7)
  num_workers: -1         # 進程數 (-1 = 全部)

output:
  save_csv: true   # 是否保存 CSV
```

### 參數影響

| 參數          | 影響                               |
| ------------- | ---------------------------------- |
| `num_samples` | 樣本數越多，結果越準確，但耗時越長 |
| `num_workers` | 進程數，建議使用 -1 自動檢測       |

### 調整建議

- **快速測試**: 減少 `num_samples` 至 100000
- **更高精度**: 增加 `num_samples` 至 100000000

---

## single_point.yaml (單點測試)

**路徑**: `simulation/config/single_point.yaml`

```yaml
description: "Single Point Detailed Simulation"

simulation:
  M: 100           # 設備總數
  N: 40            # 固定 N 值
  I_max: 10        # 最大周期數

performance:
  num_samples: 1000   # 少量樣本
  num_workers: 16     # 進程數

output:
  save_csv: true
  show_details: true  # 顯示詳細信息
```

**用途**: 快速測試和調試

---

## 配置載入方式

在代碼中使用 `load_config` 函數載入配置：

```python
from config import load_config

# 載入解析配置
config = load_config('analytical', 'figure1')

# 載入模擬配置
config = load_config('simulation', 'figure345')
```

---

[← 返回 README](../../README.md) | [使用指南 →](USER_GUIDE.md)
