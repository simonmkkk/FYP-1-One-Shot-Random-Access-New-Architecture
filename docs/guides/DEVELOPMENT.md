# 開發指南

本文檔提供項目的開發規範和擴展指南。

---

## 代碼結構原則

1. **模組解耦**: Analytical、Simulation、Plot 三模組獨立運作
2. **數據傳遞**: 通過 CSV 文件，不依賴內存
3. **配置驅動**: 所有參數由 YAML 文件控制

---

## 文檔維護要求

> ⚠️ **重要**: 任何功能更新必須同步更新文檔

### 文件夾文檔

每個文件夾需要 README.md，包含：

- 文件夾功能（3 行以內）
- 文件列表及功能說明

### 文件註釋

每個 Python 文件開頭需要：

- **Input**: 依賴的外部模組/數據
- **Output**: 對外提供的函數/類
- **Position**: 在系統中的角色

---

## 添加新 Figure 的步驟

### 1. 配置

在 `config/` 添加 YAML 文件：

```yaml
# config/analytical/figureX.yaml
description: "Figure X: 新功能"

parameters:
  M: 100
  N_start: 5
  N_stop: 50
```

### 2. 計算

在 `analytical/figure_analysis/` 或 `simulation/` 添加計算邏輯：

```python
# analytical/figure_analysis/figureX_analysis.py

def run_figureX_analysis(config: dict) -> str:
    """
    執行 Figure X 解析計算
    
    Args:
        config: 配置字典
        
    Returns:
        輸出 CSV 路徑
    """
    # 實現計算邏輯
    pass
```

### 3. 繪圖

在 `plot/` 添加繪圖函數：

```python
# plot/figureX.py

def plot_figureX(csv_path: str, output_dir: str) -> str:
    """
    繪製 Figure X
    
    Args:
        csv_path: 數據 CSV 路徑
        output_dir: 輸出目錄
        
    Returns:
        輸出 PNG 路徑
    """
    # 實現繪圖邏輯
    pass
```

### 4. 入口

在 `main.py` 添加選單和處理邏輯：

```python
# 在互動式選單中添加選項
print("  14. Figure X 完整流程")

# 在處理邏輯中添加
elif choice == '14':
    run_figureX_complete()
```

### 5. 文檔

更新以下文件：

- `README.md` - 功能概覽
- `docs/USER_GUIDE.md` - 選項說明
- `docs/OUTPUT_GUIDE.md` - 輸出格式

---

## 工作流程文檔

詳細的執行流程請參考 [`workflow/main_workflow.md`](../workflow/main_workflow.md)

---

## 代碼風格

- **Python 版本**: 3.13.9
- **格式化**: 遵循 PEP 8
- **類型提示**: 使用 type hints
- **註釋語言**: 中文

### 範例

```python
def calculate_success_probability(
    M: int, 
    N: int, 
    I_max: int
) -> tuple[float, float, float]:
    """
    計算接入成功概率
    
    Args:
        M: 設備總數
        N: RAO 數量
        I_max: 最大周期數
        
    Returns:
        (P_S, T_a, P_C) 三元組
    """
    # 初始化競爭設備數
    K = M
    
    # 迭代計算
    for i in range(1, I_max + 1):
        # ...
        pass
    
    return P_S, T_a, P_C
```

---

## 測試

### 單點測試

使用 `single_point.yaml` 配置進行快速驗證：

```bash
uv run python main.py simulation single_point
```

### 完整測試

運行所有功能：

```bash
uv run python main.py run all
```

---

[← 返回 README](../../README.md) | [性能監測 →](PERFORMANCE.md)
