# 常見問題 FAQ

本文檔收錄了常見問題及其解答。

---

## Q1: 為什麼使用 Python 3.13.9？

**A**: 本專案固定使用 Python 3.13.9 以確保環境一致性。模擬模組使用 `ProcessPoolExecutor` 進行多進程並行，可實現：

- 多核並行計算
- 高效率的蒙特卡洛模擬

---

## Q2: Figure 3-5 模擬為什麼這麼慢？

**A**: 論文要求 10^7 (1000 萬) 次模擬以確保統計可靠性。每個 N 值需要 ~140 秒，41 個 N 值總計需要 ~95-100 分鐘。

**加速建議**:

- 使用更多 CPU 核心
- 減少 `num_samples`（會降低準確性）

```yaml
# simulation/config/simulation_figure345.yaml
performance:
  num_samples: 1000000  # 從 10^7 減少到 10^6
```

---

## Q3: 運行選項 5 時顯示「找不到解析結果」？

**A**: 選項 5 會嘗試載入選項 3 的結果來計算誤差。這是可選的：

- 如果沒有解析結果，模擬仍會正常執行
- 只是不會計算誤差
- 建議先運行選項 3 再運行選項 5

---

## Q4: 繪圖時報錯「無法找到數據」？

**A**: 繪圖選項需要先運行對應的計算選項：

| 繪圖選項        | 需要先運行     |
| --------------- | -------------- |
| Figure 1 繪圖   | 選項 1         |
| Figure 2 繪圖   | 選項 2         |
| Figure 3-5 繪圖 | 選項 3 和/或 5 |

**建議**: 使用「完整流程」選項（10-13）自動處理依賴

---

## Q5: 結果目錄中有很多時間戳文件夾？

**A**: 每次運行都會創建新的時間戳目錄，這是為了：

- ✅ 保留歷史結果
- ✅ 方便對比不同運行
- ✅ 避免覆蓋之前的結果

系統會自動讀取最新的結果。如需清理，可手動刪除舊目錄。

---

## Q6: 如何修改模擬參數？

**A**: 編輯 `simulation/config/simulation_figure345.yaml`：

```yaml
performance:
  num_samples: 1000000   # 減少可加快速度
  num_workers: 8         # 指定進程數

scan:
  range:
    start: 10            # 調整 N 範圍
    stop: 30
```

---

## Q7: 圖表顯示不正常/中文亂碼？

**A**: 確保系統安裝了中文字體：

| 操作系統 | 推薦字體            | 安裝命令                              |
| -------- | ------------------- | ------------------------------------- |
| Windows  | Microsoft YaHei     | 系統已內置                            |
| macOS    | PingFang SC         | 系統已內置                            |
| Linux    | WenQuanYi Micro Hei | `sudo apt install fonts-wqy-microhei` |

或修改 `plot/common.py` 中的字體設置。

---

## Q8: 如何使用性能監測功能？

**A**: 使用 `--performance` 參數啟用性能監測：

```bash
uv run python main.py run figure1 --performance
```

運行後會在控制台顯示詳細報告，並保存 JSON 數據：
- `result/performance/{timestamp}/performance_data.json`

詳見 [性能監測文檔](PERFORMANCE.md)

---

## Q9: 性能監測報告中的指標如何解讀？

**A**: 

| 指標       | 說明                          |
| ---------- | ----------------------------- |
| 執行時間   | 函數從開始到結束的總時間      |
| 峰值內存   | 函數執行期間的最大內存使用量  |
| 內存增量   | 函數執行前後的內存變化        |
| CPU 平均值 | 函數執行期間的平均 CPU 使用率 |
| CPU 峰值   | 最高 CPU 使用率點             |

---

## Q10: uv 命令找不到？

**A**: 安裝 uv 包管理器：

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Q11: 如何查看更詳細的錯誤信息？

**A**: 運行時添加 `--verbose` 參數：

```bash
uv run python main.py run figure1 --verbose
```

---

## Q12: 能否只運行部分 N 值的模擬？

**A**: 可以，修改配置文件中的 N 範圍：

```yaml
# simulation/config/simulation_figure345.yaml
scan:
  range:
    start: 20    # 只計算 N=20 到 N=30
    stop: 31
    step: 1
```

---

[← 返回 README](../../README.md)
