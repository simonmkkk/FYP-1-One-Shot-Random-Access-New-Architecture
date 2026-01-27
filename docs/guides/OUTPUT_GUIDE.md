# 輸出結果說明

本文檔詳細說明所有輸出文件的格式和結構。

---

## CSV 文件格式

### figure1_N{n}.csv

**路徑**: `result/analytical/figure1/{timestamp}/`

```csv
M,M/N,analytical_N_S,analytical_N_C,approx_N_S,approx_N_C
1,0.333,0.222,0.000,0.238,0.000
2,0.667,0.395,0.049,0.422,0.070
3,1.000,0.522,0.111,0.552,0.148
...
```

| 欄位           | 類型  | 說明             |
| -------------- | ----- | ---------------- |
| M              | int   | 設備數           |
| M/N            | float | M/N 比值         |
| analytical_N_S | float | 精確公式 N_S,1/N |
| analytical_N_C | float | 精確公式 N_C,1/N |
| approx_N_S     | float | 近似公式 N_S,1/N |
| approx_N_C     | float | 近似公式 N_C,1/N |

---

### figure2_N{n}.csv

**路徑**: `result/analytical/figure2/{timestamp}/`

```csv
M,M/N,analytical_N_S,analytical_N_C,approx_N_S,approx_N_C,N_S_error(%),N_C_error(%)
1,0.333,0.222,0.000,0.238,0.000,7.23,0.00
2,0.667,0.395,0.049,0.422,0.070,6.84,42.86
...
```

| 欄位         | 類型  | 說明           |
| ------------ | ----- | -------------- |
| N_S_error(%) | float | N_S 誤差百分比 |
| N_C_error(%) | float | N_C 誤差百分比 |

---

### figure345_analytical.csv

**路徑**: `result/analytical/figure345/{timestamp}/`

```csv
N,P_S,T_a,P_C,M,I_max
5,0.369,4.832,0.584,100,10
6,0.452,4.215,0.542,100,10
...
45,0.998,1.078,0.045,100,10
```

| 欄位  | 類型  | 說明         |
| ----- | ----- | ------------ |
| N     | int   | RAO 數量     |
| P_S   | float | 接入成功概率 |
| T_a   | float | 平均接入延遲 |
| P_C   | float | 碰撞概率     |
| M     | int   | 設備總數     |
| I_max | int   | 最大周期數   |

---

### figure345_simulation.csv

**路徑**: `result/simulation/figure345/{timestamp}/`

```csv
N,P_S,T_a,P_C,P_S_error,T_a_error,P_C_error,M,I_max
5,0.368,4.831,0.583,0.27,0.02,0.17,100,10
6,0.451,4.213,0.541,0.22,0.05,0.18,100,10
...
```

| 欄位      | 類型  | 說明           |
| --------- | ----- | -------------- |
| P_S_error | float | P_S 誤差百分比 |
| T_a_error | float | T_a 誤差百分比 |
| P_C_error | float | P_C 誤差百分比 |

---

## 圖表輸出說明

### Figure 1: 精確 vs 近似

- **佈局**: 2 行，上面 3 個子圖，下面 1 個合併圖
- **線條樣式**:
  - N=3: 實線+圓圈（N_S）、點線+圓圈（N_C）
  - N=14: 實線無標記（N_S）、虛線無標記（N_C）
  - 近似: 細點線（N_S）、點劃線（N_C）

### Figure 2: 誤差分析

- **Y 軸**: 對數刻度（1e-2 到 1e3）
- **線條**: 與 Figure 1 對應

### Figure 3-5: 性能指標

- **雙 Y 軸**:
  - 左軸（藍色）: 性能指標值
  - 右軸（綠色）: 近似誤差 (%)
- **線條樣式**:
  - 實線: 理論曲線
  - 空心圓: 模擬結果
  - 虛線: 誤差曲線

---

## 結果目錄結構

```
result/
├── analytical/
│   ├── figure1/
│   │   └── 20260106_143022/
│   │       ├── figure1_N3.csv
│   │       └── figure1_N14.csv
│   ├── figure2/
│   │   └── 20260106_143025/
│   │       ├── figure2_N3.csv
│   │       └── figure2_N14.csv
│   └── figure345/
│       └── 20260106_143030/
│           └── figure345_analytical.csv
│
├── simulation/
│   └── figure345/
│       └── 20260106_153045/
│           └── figure345_simulation.csv
│
└── graph/
    ├── figure1/
    │   └── 20260106_143027/
    │       └── figure1.png
    ├── figure2/
    │   └── 20260106_143028/
    │       └── figure2.png
    ├── figure3/
    │   └── 20260106_153050/
    │       └── figure3.png
    ├── figure4/
    │   └── 20260106_153051/
    │       └── figure4.png
    └── figure5/
        └── 20260106_153052/
            └── figure5.png
```

---

## 時間戳說明

每次運行都會創建新的時間戳目錄（格式：`YYYYMMDD_HHMMSS`），這是為了：

- ✅ 保留歷史結果
- ✅ 方便對比不同運行
- ✅ 避免覆蓋之前的結果

系統會自動讀取最新的結果。如需清理，可手動刪除舊目錄。

---

[← 返回 README](../../README.md) | [開發指南 →](DEVELOPMENT.md)
