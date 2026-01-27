# 性能監測文檔

本文檔說明系統內置的性能監測功能。

---

## 功能概述

系統內置性能監測功能，可測量所有關鍵函數的：

- **執行時間**: 精確到毫秒
- **內存使用**: 峰值和增量（MB）
- **CPU 使用率**: 平均和峰值（%）

---

## 快速使用

### CLI 模式

```bash
# 啟用性能監測運行 Figure 1
uv run python main.py run figure1 --performance

# 啟用性能監測運行完整流程
uv run python main.py run all --performance

# 指定報告保存路徑
uv run python main.py run figure345 --performance --performance-report ./my_reports
```

### 程序化使用

```python
from performance import (
    performance_monitor, 
    start_monitoring, 
    stop_monitoring, 
    generate_performance_report
)

# 方式 1: 使用裝飾器
@performance_monitor(level='workflow', name='My Workflow')
def my_function():
    pass

# 方式 2: 手動控制
start_monitoring()
# ... 執行代碼 ...
stop_monitoring()
generate_performance_report()
```

---

## 監測級別

| 級別       | 說明       | 適用場景         |
| ---------- | ---------- | ---------------- |
| `function` | 函數級別   | 細粒度分析       |
| `module`   | 模組級別   | 分析模組整體性能 |
| `workflow` | 工作流級別 | 分析完整流程     |

---

## 輸出

運行後自動生成：

### 控制台報告

```
╔══════════════════════════════════════════════════════════════╗
║                    Performance Report                        ║
╠══════════════════════════════════════════════════════════════╣
║  Total Execution Time: 125.3s                                ║
║  Peak Memory Usage: 512.4 MB                                 ║
║  Average CPU Usage: 85.2%                                    ║
╚══════════════════════════════════════════════════════════════╝

Top 10 Time-Consuming Functions:
┌────────────────────────────┬──────────┬─────────┐
│ Function                   │ Time (s) │ % Total │
├────────────────────────────┼──────────┼─────────┤
│ run_simulation             │ 95.2     │ 76.0%   │
│ calculate_metrics          │ 15.3     │ 12.2%   │
│ plot_figures               │ 8.1      │ 6.5%    │
└────────────────────────────┴──────────┴─────────┘
```

### JSON 數據

**路徑**: `result/performance/{timestamp}/performance_data.json`

```json
{
  "total_time": 125.3,
  "peak_memory_mb": 512.4,
  "avg_cpu_percent": 85.2,
  "functions": [
    {
      "name": "run_simulation",
      "level": "workflow",
      "time_seconds": 95.2,
      "memory_delta_mb": 256.1,
      "cpu_avg_percent": 92.3
    }
  ]
}
```

---

## 報告解讀

### 執行時間

- 函數從開始到結束的總時間
- 包含所有子函數調用時間

### 峰值內存

- 函數執行期間的最大內存使用量
- 用於識別內存密集型操作

### 內存增量

- 函數執行前後的內存變化
- 正值表示有內存分配
- 負值表示有內存釋放

### CPU 使用率

- **平均值**: 函數執行期間的平均 CPU 使用率
- **峰值**: 最高 CPU 使用率點

---

## 性能開銷

> ⚠️ **注意**: 性能監測會帶來約 **2-5%** 的性能開銷

建議僅在需要分析時啟用，不要在生產運行時常態開啟。

---

## 常見用途

### 識別瓶頸

查看 Top 10 耗時函數，找出性能瓶頸。

### 內存優化

監測內存使用，識別內存洩漏或過度分配。

### 並行效率

比較 CPU 使用率，評估多進程並行效率。

---

[← 返回 README](../../README.md) | [常見問題 →](FAQ.md)
