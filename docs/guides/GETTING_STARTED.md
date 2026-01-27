# 詳細安裝與首次運行指南

本文檔提供完整的環境設置和首次運行說明。

---

## 環境要求

| 要求         | 版本                    | 說明                       |
| ------------ | ----------------------- | -------------------------- |
| **Python**   | 3.13.9                  | 使用 uv 會自動安裝正確版本 |
| **包管理器** | uv (推薦) 或 pip        | uv 更快更現代              |
| **操作系統** | Windows / macOS / Linux | 全平台支持                 |

### 關於 Python 版本

本專案使用 Python 3.13.9。模擬模組使用 `ProcessPoolExecutor` 進行多進程並行計算，配合 **Batch Optimization** 策略，可實現：

- 🚀 多核並行計算（使用 Batch 分塊策略減少 IPC 開銷）
- ⏱️ 高吞吐量的蒙特卡洛模擬（~40,000 樣本/秒）
- 💪 10^7 樣本約 4 分鐘完成

---

## 安裝步驟

### Step 1: 克隆項目

```bash
git clone <repository-url>
cd FYP-1-One-Shot-Random-Access-New-Architecture
```

### Step 2: 安裝依賴

#### 方式一：使用 uv（推薦）

```bash
uv sync
```

#### 方式二：使用 pip

```bash
pip install numpy==2.3.5 matplotlib==3.10.7 tqdm==4.67.1 pyyaml==6.0.3
```

---

## 運行系統

### 方式一：互動式選單（推薦新手）

```bash
uv run python main.py
```

將看到以下選單：

```
======================================================================
One-Shot Random Access 模擬與分析系統
======================================================================

請選擇操作:

【解析計算 (Analytical)】
   1. Figure 1: NS,1/N & NC,1/N 精確公式 + 近似公式
   2. Figure 2: 近似誤差分析（精確 vs 近似）
   3. Figure 3, 4, 5 合併解析 (P_S, T_a, P_C)
   4. 運行所有解析計算

【模擬 (Simulation)】
   5. Figure 3, 4, 5 合併模擬 (P_S, T_a, P_C)

【繪圖 (Plot)】
   6. 繪製 Figure 1
   7. 繪製 Figure 2
   8. 繪製 Figure 3, 4, 5
   9. 繪製所有圖表

【完整流程】
  10. Figure 1 完整流程 (Analytical + Plot)
  11. Figure 2 完整流程 (Analytical + Plot)
  12. Figure 3, 4, 5 完整流程 (Analytical + Simulation + Plot)
  13. 所有圖表完整流程

   0. 退出
======================================================================
```

### 方式二：CLI 命令行

```bash
# 解析計算
uv run python main.py analytical figure1        # Figure 1 解析
uv run python main.py analytical figure2        # Figure 2 解析
uv run python main.py analytical figure345      # Figure 3-5 解析
uv run python main.py analytical all            # 所有解析

# 模擬
uv run python main.py simulation figure345      # Figure 3-5 模擬

# 繪圖
uv run python main.py plot figure1              # 繪製 Figure 1
uv run python main.py plot figure2              # 繪製 Figure 2
uv run python main.py plot figure345            # 繪製 Figure 3-5
uv run python main.py plot all                  # 繪製所有

# 完整流程
uv run python main.py run figure1               # Figure 1 完整
uv run python main.py run figure2               # Figure 2 完整
uv run python main.py run figure345             # Figure 3-5 完整
uv run python main.py run all                   # 所有完整
```

---

## 推薦的首次運行

**對於新手**，建議按以下順序執行：

```bash
# 1. 先運行 Figure 1 完整流程（最快，約 1-2 分鐘）
uv run python main.py run figure1

# 2. 查看生成的圖表
# 輸出位置: result/graph/figure1/{時間戳}/figure1.png

# 3. 如果想體驗完整功能，運行 Figure 3-5（較慢，模擬約 2-3 分鐘/N值）
uv run python main.py run figure345
```

---

## 常見安裝問題

### Q: uv 命令找不到？

安裝 uv：

```bash
# Windows (PowerShell)
irm https://astral.sh/uv/install.ps1 | iex

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Q: Python 版本不對？

使用 uv 會自動安裝正確版本，無需手動管理。

### Q: 圖表中文顯示亂碼？

確保系統安裝了中文字體：
- Windows: Microsoft YaHei
- macOS: PingFang SC
- Linux: `sudo apt install fonts-wqy-microhei`

---

[← 返回 README](../../README.md)
