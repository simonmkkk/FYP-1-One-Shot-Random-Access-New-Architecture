# Main Workflow Documentation

本文档描述从 `main.py` 开始的每个菜单选项的完整执行流程，包括所有调用的文件和模块。

## 入口点

**文件**: `main.py`

- **函数**: `main()` → `interactive_menu()` 或 CLI 命令处理
- **作用**: 系统主入口，提供交互式菜单和命令行接口

---

## 菜单选项执行流程

### 【解析计算 (Analytical)】

#### 选项 1: Figure 1 - NS,1/N & NC,1/N 精确公式 + 近似公式

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 1]) --> Main[main.py: run_analytical_figure1]
    Main --> LoadConfig[config/loader/loader.py: load_config]
    LoadConfig --> ReadYAML[读取 config/analytical/figure1.yaml]
    ReadYAML --> RunAnalysis[analytical/figure_analysis/figure1_analysis.py: run_figure1_analysis]
    RunAnalysis --> Formula2[formulas.py: paper_formula_2_collision_raos_exact]
    RunAnalysis --> Formula3[formulas.py: paper_formula_3_success_raos_exact]
    RunAnalysis --> Formula4[formulas.py: paper_formula_4_success_approx]
    RunAnalysis --> Formula5[formulas.py: paper_formula_5_collision_approx]
    Formula2 --> SaveCSV[保存 CSV 文件]
    Formula3 --> SaveCSV
    Formula4 --> SaveCSV
    Formula5 --> SaveCSV
    SaveCSV --> End([完成: result/analytical/figure1/YYYYMMDD_HHMMSS/figure1_analysis.csv])
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style RunAnalysis fill:#ffccbc
```

**文件调用树**:

```text
main.py
└── run_analytical_figure1()
    ├── config/loader/loader.py
    │   └── load_config('analytical', 'figure1')
    │       └── 读取: config/analytical/figure1.yaml
    └── analytical/figure_analysis/figure1_analysis.py
        └── run_figure1_analysis(config)
            ├── analytical/formulas/formulas.py
            │   ├── paper_formula_2_collision_raos_exact()  [精确公式]
            │   ├── paper_formula_3_success_raos_exact()    [精确公式]
            │   ├── paper_formula_4_success_approx()        [近似公式]
            │   └── paper_formula_5_collision_approx()      [近似公式]
            └── 保存结果到: result/analytical/figure1/YYYYMMDD_HHMMSS/figure1_analysis.csv
```

**调用的文件**:

- `main.py` (line 141-144)
- `config/loader/loader.py` - 加载配置
- `config/analytical/figure1.yaml` - 配置文件
- `analytical/figure_analysis/figure1_analysis.py` - 主要计算逻辑
- `analytical/formulas/formulas.py` - 公式实现

**输出文件**:

- `result/analytical/figure1/YYYYMMDD_HHMMSS/figure1_analysis.csv`

---

#### 选项 2: Figure 2 - 近似误差分析（精确 vs 近似）

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 2]) --> Main[main.py: run_analytical_figure2]
    Main --> LoadConfig[config/loader/loader.py: load_config]
    LoadConfig --> ReadYAML[读取 config/analytical/figure1.yaml]
    ReadYAML --> RunAnalysis[analytical/figure_analysis/figure2_analysis.py: run_figure2_analysis]
    RunAnalysis --> LoadFig1{加载 Figure 1 结果}
    LoadFig1 -->|优先| UseParam[使用传入的 fig1_data]
    LoadFig1 -->|其次| LoadCSV[load_figure1_results: 读取 CSV]
    LoadFig1 -->|最后| Recalc[重新运行 Figure 1]
    UseParam --> CalcError["计算误差: abs(Analytical - Approximation) / abs(Analytical) * 100%"]
    LoadCSV --> CalcError
    Recalc --> CalcError
    CalcError --> SaveCSV[保存 CSV 文件]
    SaveCSV --> End([完成: result/analytical/figure2/YYYYMMDD_HHMMSS/figure2_analysis.csv])
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style RunAnalysis fill:#ffccbc
    style LoadFig1 fill:#e1bee7
```

**文件调用树**:

```text
main.py
└── run_analytical_figure2()
    ├── config/loader/loader.py
    │   └── load_config('analytical', 'figure1')  [使用 Figure 1 配置]
    │       └── 读取: config/analytical/figure1.yaml
    └── analytical/figure_analysis/figure2_analysis.py
        └── run_figure2_analysis(config)
            ├── analytical/figure_analysis/figure1_analysis.py
            │   └── load_figure1_results()
            │       └── 读取: result/analytical/figure1/最新时间戳/figure1_analysis.csv
            ├── 计算误差: |Analytical - Approximation| / |Analytical| * 100%
            └── 保存结果到: result/analytical/figure2/YYYYMMDD_HHMMSS/figure2_analysis.csv
```

**调用的文件**:

- `main.py` (line 147-153)
- `config/loader/loader.py` - 加载配置
- `config/analytical/figure1.yaml` - 配置文件
- `analytical/figure_analysis/figure2_analysis.py` - 主要计算逻辑
- `analytical/figure_analysis/figure1_analysis.py` - 加载 Figure 1 数据

**输出文件**:

- `result/analytical/figure2/YYYYMMDD_HHMMSS/figure2_analysis.csv`

---

#### 选项 3: Figure 3, 4, 5 合并解析 (P_S, T_a, P_C)

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 3]) --> Main[main.py: run_analytical_figure345]
    Main --> LoadConfig[config/loader/loader.py: load_config]
    LoadConfig --> ReadYAML[读取 config/analytical/figure345.yaml]
    ReadYAML --> RunAnalysis[analytical/figure_analysis/figure345_analysis.py: run_figure345_analysis]
    RunAnalysis --> Theoretical[analytical/theoretical/theoretical.py: theoretical_calculation]
    Theoretical --> Loop[循环每个 N 值]
    Loop --> Formula5[formulas.py: paper_formula_5_collision_approx]
    Loop --> Formula6[formulas.py: paper_formula_6_success_per_cycle]
    Loop --> Formula7[formulas.py: paper_formula_7_next_contending_devices]
    Formula5 --> Formula8[formulas.py: paper_formula_8_access_success_probability]
    Formula6 --> Formula8
    Formula7 --> Formula8
    Formula8 --> Formula9[formulas.py: paper_formula_9_mean_access_delay]
    Formula8 --> Formula10[formulas.py: paper_formula_10_collision_probability]
    Formula9 --> SaveCSV[保存 CSV 文件]
    Formula10 --> SaveCSV
    SaveCSV --> End([完成: result/analytical/figure345/YYYYMMDD_HHMMSS/figure345_analysis.csv])
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style RunAnalysis fill:#ffccbc
    style Theoretical fill:#b2dfdb
    style Loop fill:#e1bee7
```

**文件调用树**:

```text
main.py
└── run_analytical_figure345()
    ├── config/loader/loader.py
    │   └── load_config('analytical', 'figure345')
    │       └── 读取: config/analytical/figure345.yaml
    └── analytical/figure_analysis/figure345_analysis.py
        └── run_figure345_analysis(config)
            └── analytical/theoretical/theoretical.py
                └── theoretical_calculation(M, N, I_max)
                    └── analytical/formulas/formulas.py
                        ├── paper_formula_5_collision_approx()   [Eq. 5]
                        ├── paper_formula_6_success_per_cycle()   [Eq. 6]
                        ├── paper_formula_7_next_contending_devices() [Eq. 7]
                        ├── paper_formula_8_access_success_probability() [Eq. 8]
                        ├── paper_formula_9_mean_access_delay()  [Eq. 9]
                        └── paper_formula_10_collision_probability() [Eq. 10]
            └── 保存结果到: result/analytical/figure345/YYYYMMDD_HHMMSS/figure345_analysis.csv
```

**调用的文件**:

- `main.py` (line 156-159)
- `config/loader/loader.py` - 加载配置
- `config/analytical/figure345.yaml` - 配置文件
- `analytical/figure_analysis/figure345_analysis.py` - 主要计算逻辑
- `analytical/theoretical/theoretical.py` - 理论计算
- `analytical/formulas/formulas.py` - 公式实现 (Eq. 5-10)

**输出文件**:

- `result/analytical/figure345/YYYYMMDD_HHMMSS/figure345_analysis.csv`

---

#### 选项 4: 运行所有解析计算

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 4]) --> Main[main.py: run_analytical_all]
    Main --> Step1[步骤 1: run_analytical_figure1]
    Step1 --> Step2[步骤 2: run_analytical_figure2]
    Step2 --> Step3[步骤 3: run_analytical_figure345]
    Step1 --> Fig1Result[Figure 1 结果]
    Fig1Result --> Step2
    Step2 --> Fig2Result[Figure 2 结果]
    Step3 --> Fig345Result[Figure 3-5 结果]
    Fig1Result --> End([完成: 所有解析结果])
    Fig2Result --> End
    Fig345Result --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Step1 fill:#ffccbc
    style Step2 fill:#ffccbc
    style Step3 fill:#ffccbc
```

**文件调用树**:

```text
main.py
└── run_analytical_all()
    ├── [1] run_analytical_figure1()  [见选项 1]
    │   └── ... (选项 1 的所有调用)
    ├── [2] run_analytical_figure2(config, fig1_data=fig1_data)  [见选项 2，传入 Figure 1 结果]
    │   └── ... (选项 2 的所有调用)
    └── [3] run_analytical_figure345()  [见选项 3]
        └── ... (选项 3 的所有调用)
```

**调用的文件**:

- `main.py` (line 162-179)
- 所有选项 1、2、3 调用的文件

**输出文件**:

- 选项 1、2、3 的所有输出文件

---

### 【模拟 (Simulation)】

#### 选项 5: Figure 3, 4, 5 合并模拟 (P_S, T_a, P_C)

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 5]) --> Main[main.py: run_simulation_figure345]
    Main --> LoadConfig[config/loader/loader.py: load_config]
    LoadConfig --> ReadYAML[读取 config/simulation/figure345.yaml]
    ReadYAML --> RunSim[simulation/figure_simulation/figure345_simulation.py: run_figure345_simulation]
    RunSim --> LoopN[循环每个 N 值]
    LoopN --> GroupPaging[simulation/core/group_paging.py: simulate_group_paging_multi_samples]
    GroupPaging --> Parallel[ThreadPoolExecutor 多线程并行]
    Parallel --> OneShot[simulation/core/one_shot_access.py: simulate_one_shot_access_single_sample]
    OneShot --> RandomNum[numpy.random 生成随机数]
    RandomNum --> Parallel
    Parallel --> Metrics[simulation/core/metrics.py: calculate_performance_metrics]
    Metrics --> LoadAnalytical{加载解析结果}
    LoadAnalytical -->|存在| CalcError[计算 Approximation Error]
    LoadAnalytical -->|不存在| Warn[警告但不影响]
    CalcError --> SaveCSV[保存 CSV 文件]
    Warn --> SaveCSV
    SaveCSV --> End([完成: result/simulation/figure345/YYYYMMDD_HHMMSS/figure345_simulation.csv])
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style RunSim fill:#ffccbc
    style GroupPaging fill:#b2dfdb
    style Parallel fill:#e1bee7
    style LoadAnalytical fill:#fff9c4
```

**文件调用树**:

```text
main.py
└── run_simulation_figure345()
    ├── config/loader/loader.py
    │   └── load_config('simulation', 'figure345')
    │       └── 读取: config/simulation/figure345.yaml
    └── simulation/figure_simulation/figure345_simulation.py
        └── run_figure345_simulation(config)
            ├── simulation/core/group_paging.py
            │   └── simulate_group_paging_multi_samples(M, N, I_max, num_samples, num_workers)
            │       ├── ThreadPoolExecutor 多线程并行执行
            │       └── simulation/core/one_shot_access.py
            │           └── simulate_one_shot_access_single_sample()
            │               └── numpy.random 生成随机数
            ├── simulation/core/metrics.py
            │   └── calculate_performance_metrics(results_array)
            │       └── 计算 P_S, T_a, P_C 的均值和置信区间
            ├── analytical/figure_analysis/figure345_analysis.py
            │   └── load_figure345_results()  [加载解析结果]
            │       └── 读取: result/analytical/figure345/最新时间戳/figure345_analysis.csv
            ├── 计算 Approximation Error: |Approximation - Simulation| / |Approximation| * 100%
            └── 保存结果到: result/simulation/figure345/YYYYMMDD_HHMMSS/figure345_simulation.csv
```

**调用的文件**:

- `main.py` (line 187-190)
- `config/loader/loader.py` - 加载配置
- `config/simulation/figure345.yaml` - 配置文件
- `simulation/figure_simulation/figure345_simulation.py` - 模拟协调层
- `simulation/core/group_paging.py` - 群组寻呼模拟引擎
- `simulation/core/one_shot_access.py` - 单次接入模拟
- `simulation/core/metrics.py` - 性能指标计算
- `analytical/figure_analysis/figure345_analysis.py` - 加载解析结果

**输出文件**:

- `result/simulation/figure345/YYYYMMDD_HHMMSS/figure345_simulation.csv`

---

### 【绘图 (Plot)】

#### 选项 6: 绘制 Figure 1

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 6]) --> Main[main.py: run_plot_figure1]
    Main --> LoadData[analytical/figure_analysis/figure1_analysis.py: load_figure1_results]
    LoadData --> CheckData{数据是否存在?}
    CheckData -->|否| Error[错误: 请先运行选项 1]
    CheckData -->|是| ReadCSV[读取: result/analytical/figure1/最新时间戳/figure1_analysis.csv]
    ReadCSV --> Plot[plot/figure1.py: plot_figure1]
    Plot --> ExtractN[plot/common.py: extract_n_values_from_data]
    ExtractN --> Matplotlib[matplotlib.pyplot 绘制图表]
    Matplotlib --> SavePNG[保存 PNG 文件]
    SavePNG --> End([完成: result/graph/figure1/YYYYMMDD_HHMMSS/figure1.png])
    Error --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Plot fill:#ffccbc
    style CheckData fill:#e1bee7
    style Error fill:#ffcdd2
```

**文件调用树**:

```text
main.py
└── run_plot_figure1()
    ├── analytical/figure_analysis/figure1_analysis.py
    │   └── load_figure1_results()
    │       └── 读取: result/analytical/figure1/最新时间戳/figure1_analysis.csv
    └── plot/figure1.py
        └── plot_figure1(data, save_path, show)
            ├── plot/common.py
            │   └── extract_n_values_from_data()  [提取 N 值]
            └── matplotlib.pyplot 绘制图表
            └── 保存图片到: result/graph/figure1/YYYYMMDD_HHMMSS/figure1.png
```

**调用的文件**:

- `main.py` (line 201-211)
- `analytical/figure_analysis/figure1_analysis.py` - 加载数据
- `plot/figure1.py` - 绘图逻辑
- `plot/common.py` - 共用工具函数

**输出文件**:

- `result/graph/figure1/YYYYMMDD_HHMMSS/figure1.png`

---

#### 选项 7: 绘制 Figure 2

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 7]) --> Main[main.py: run_plot_figure2]
    Main --> LoadData[analytical/figure_analysis/figure2_analysis.py: load_figure2_results]
    LoadData --> CheckData{数据是否存在?}
    CheckData -->|否| Error[错误: 请先运行选项 2]
    CheckData -->|是| ReadCSV[读取: result/analytical/figure2/最新时间戳/figure2_analysis.csv]
    ReadCSV --> Plot[plot/figure2.py: plot_figure2]
    Plot --> Matplotlib[matplotlib.pyplot 绘制图表]
    Matplotlib --> SavePNG[保存 PNG 文件]
    SavePNG --> End([完成: result/graph/figure2/YYYYMMDD_HHMMSS/figure2.png])
    Error --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Plot fill:#ffccbc
    style CheckData fill:#e1bee7
    style Error fill:#ffcdd2
```

**文件调用树**:

```text
main.py
└── run_plot_figure2()
    ├── analytical/figure_analysis/figure2_analysis.py
    │   └── load_figure2_results()
    │       └── 读取: result/analytical/figure2/最新时间戳/figure2_analysis.csv
    └── plot/figure2.py
        └── plot_figure2(data, save_path, show)
            └── matplotlib.pyplot 绘制图表
            └── 保存图片到: result/graph/figure2/YYYYMMDD_HHMMSS/figure2.png
```

**调用的文件**:

- `main.py` (line 214-224)
- `analytical/figure_analysis/figure2_analysis.py` - 加载数据
- `plot/figure2.py` - 绘图逻辑

**输出文件**:

- `result/graph/figure2/YYYYMMDD_HHMMSS/figure2.png`

---

#### 选项 8: 绘制 Figure 3, 4, 5

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 8]) --> Main[main.py: run_plot_figure345]
    Main --> Fig3[处理 Figure 3]
    Fig3 --> LoadAnalytical3[加载解析数据]
    Fig3 --> LoadSimulation3[加载模拟数据]
    LoadAnalytical3 --> Plot3[plot/figure345.py: plot_figure3]
    LoadSimulation3 --> Plot3
    Plot3 --> Save3[保存 figure3.png]
    
    Main --> Fig4[处理 Figure 4]
    Fig4 --> LoadAnalytical4[加载解析数据]
    Fig4 --> LoadSimulation4[加载模拟数据]
    LoadAnalytical4 --> Plot4[plot/figure345.py: plot_figure4]
    LoadSimulation4 --> Plot4
    Plot4 --> Save4[保存 figure4.png]
    
    Main --> Fig5[处理 Figure 5]
    Fig5 --> LoadAnalytical5[加载解析数据]
    Fig5 --> LoadSimulation5[加载模拟数据]
    LoadAnalytical5 --> Plot5[plot/figure345.py: plot_figure5]
    LoadSimulation5 --> Plot5
    Plot5 --> Save5[保存 figure5.png]
    
    Save3 --> End([完成: 3个PNG文件])
    Save4 --> End
    Save5 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Fig3 fill:#ffccbc
    style Fig4 fill:#ffccbc
    style Fig5 fill:#ffccbc
```

**文件调用树**:

```text
main.py
└── run_plot_figure345()
    ├── [Figure 3]
    │   ├── main._get_analytical_data_for_figure('figure3')
    │   │   └── analytical/figure_analysis/figure345_analysis.py
    │   │       └── load_figure345_results()
    │   │           └── 读取: result/analytical/figure345/最新时间戳/figure345_analysis.csv
    │   ├── main._get_simulation_data_for_figure('figure3')
    │   │   └── simulation/figure_simulation/figure345_simulation.py
    │   │       └── load_figure345_simulation_results()
    │   │           └── 读取: result/simulation/figure345/最新时间戳/figure345_simulation.csv
    │   └── plot/figure345.py
    │       └── plot_figure3(analytical_data, simulation_data, save_path, show)
    │           └── matplotlib.pyplot 绘制图表
    │           └── 保存图片到: result/graph/figure3/YYYYMMDD_HHMMSS/figure3.png
    ├── [Figure 4] 类似流程
    │   └── plot_figure4()
    │       └── 保存图片到: result/graph/figure4/YYYYMMDD_HHMMSS/figure4.png
    └── [Figure 5] 类似流程
        └── plot_figure5()
            └── 保存图片到: result/graph/figure5/YYYYMMDD_HHMMSS/figure5.png
```

**调用的文件**:

- `main.py` (line 227-260)
- `analytical/figure_analysis/figure345_analysis.py` - 加载解析数据
- `simulation/figure_simulation/figure345_simulation.py` - 加载模拟数据
- `plot/figure345.py` - 绘图逻辑

**输出文件**:

- `result/graph/figure3/YYYYMMDD_HHMMSS/figure3.png`
- `result/graph/figure4/YYYYMMDD_HHMMSS/figure4.png`
- `result/graph/figure5/YYYYMMDD_HHMMSS/figure5.png`

---

#### 选项 9: 绘制所有图表

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 9]) --> Main[main.py: run_plot_all]
    Main --> Plot1[run_plot_figure1 show=False]
    Main --> Plot2[run_plot_figure2 show=False]
    Main --> Plot3[run_plot_figure345 show=True]
    Plot1 --> End([完成: 所有图表])
    Plot2 --> End
    Plot3 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Plot1 fill:#ffccbc
    style Plot2 fill:#ffccbc
    style Plot3 fill:#ffccbc
```

**文件调用树**:

```text
main.py
└── run_plot_all()
    ├── run_plot_figure1(show=False)  [见选项 6]
    ├── run_plot_figure2(show=False)  [见选项 7]
    └── run_plot_figure345(show=True)  [见选项 8]
```

**调用的文件**:

- `main.py` (line 263-272)
- 所有选项 6、7、8 调用的文件

**输出文件**:

- 选项 6、7、8 的所有输出文件

---

### 【完整流程】

#### 选项 10: Figure 1 完整流程 (Analytical + Plot)

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 10]) --> Main[main.py: run_pipeline_figure1]
    Main --> Step1[步骤 1/2: run_analytical_figure1]
    Step1 --> Step2[步骤 2/2: run_plot_figure1]
    Step1 --> End([完成: CSV + PNG])
    Step2 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Step1 fill:#ffccbc
    style Step2 fill:#b2dfdb
```

**文件调用树**:

```text
main.py
└── run_pipeline_figure1()
    ├── [1/2] run_analytical_figure1()  [见选项 1]
    └── [2/2] run_plot_figure1()  [见选项 6]
```

**调用的文件**:

- `main.py` (line 283-297)
- 选项 1 和选项 6 的所有文件

**输出文件**:

- 选项 1 和选项 6 的所有输出文件

---

#### 选项 11: Figure 2 完整流程 (Analytical + Plot)

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 11]) --> Main[main.py: run_pipeline_figure2]
    Main --> Step1[步骤 1/2: run_analytical_figure2]
    Step1 --> Step2[步骤 2/2: run_plot_figure2]
    Step1 --> End([完成: CSV + PNG])
    Step2 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Step1 fill:#ffccbc
    style Step2 fill:#b2dfdb
```

**文件调用树**:

```text
main.py
└── run_pipeline_figure2()
    ├── [1/2] run_analytical_figure2()  [见选项 2]
    └── [2/2] run_plot_figure2()  [见选项 7]
```

**调用的文件**:

- `main.py` (line 300-314)
- 选项 2 和选项 7 的所有文件

**输出文件**:

- 选项 2 和选项 7 的所有输出文件

---

#### 选项 12: Figure 3, 4, 5 完整流程 (Analytical + Simulation + Plot)

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 12]) --> Main[main.py: run_pipeline_figure345]
    Main --> Step1[步骤 1/3: run_analytical_figure345]
    Step1 --> Step2[步骤 2/3: run_simulation_figure345]
    Step2 --> Step3[步骤 3/3: run_plot_figure345]
    Step1 --> End([完成: CSV + CSV + PNGs])
    Step2 --> End
    Step3 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Step1 fill:#ffccbc
    style Step2 fill:#b2dfdb
    style Step3 fill:#c5cae9
```

**文件调用树**:

```text
main.py
└── run_pipeline_figure345()
    ├── [1/3] run_analytical_figure345()  [见选项 3]
    ├── [2/3] run_simulation_figure345()  [见选项 5]
    └── [3/3] run_plot_figure345()  [见选项 8]
```

**调用的文件**:

- `main.py` (line 317-334)
- 选项 3、5、8 的所有文件

**输出文件**:

- 选项 3、5、8 的所有输出文件

---

#### 选项 13: 所有图表完整流程

**执行流程图**:

```mermaid
flowchart TD
    Start([用户选择选项 13]) --> Main[main.py: run_pipeline_all]
    Main --> Pipeline1[run_pipeline_figure1]
    Main --> Pipeline2[run_pipeline_figure2]
    Main --> Pipeline3[run_pipeline_figure345]
    Pipeline1 --> End([完成: 所有结果])
    Pipeline2 --> End
    Pipeline3 --> End
    
    style Start fill:#e1f5ff
    style End fill:#c8e6c9
    style Main fill:#fff9c4
    style Pipeline1 fill:#ffccbc
    style Pipeline2 fill:#ffccbc
    style Pipeline3 fill:#ffccbc
```

**文件调用树**:

```text
main.py
└── run_pipeline_all()
    ├── run_pipeline_figure1()  [见选项 10]
    ├── run_pipeline_figure2()  [见选项 11]
    └── run_pipeline_figure345()  [见选项 12]
```

**调用的文件**:

- `main.py` (line 337-341)
- 所有选项 10、11、12 调用的文件

**输出文件**:

- 所有选项 10、11、12 的输出文件

---

## 数据流向总结

### 解析计算流程

```mermaid
flowchart LR
    YAML[配置文件 YAML] --> Loader[config/loader/loader.py]
    Loader --> Formulas[formulas.py 或 theoretical.py]
    Formulas --> Analysis[figure_analysis/*.py]
    Analysis --> CSV[CSV 文件<br/>result/analytical/*/]
    
    style YAML fill:#e3f2fd
    style Loader fill:#fff9c4
    style Formulas fill:#ffccbc
    style Analysis fill:#c8e6c9
    style CSV fill:#f3e5f5
```

### 模拟流程

```mermaid
flowchart LR
    YAML[配置文件 YAML] --> Loader[config/loader/loader.py]
    Loader --> OneShot[one_shot_access.py<br/>单次接入]
    OneShot --> GroupPaging[group_paging.py<br/>多周期]
    GroupPaging --> Metrics[metrics.py<br/>性能指标]
    Metrics --> Coord[figure345_simulation.py<br/>协调层]
    Coord --> CSV[CSV 文件<br/>result/simulation/*/]
    
    style YAML fill:#e3f2fd
    style Loader fill:#fff9c4
    style OneShot fill:#b2dfdb
    style GroupPaging fill:#b2dfdb
    style Metrics fill:#b2dfdb
    style Coord fill:#ffccbc
    style CSV fill:#f3e5f5
```

### 绘图流程

```mermaid
flowchart LR
    CSV1[CSV 文件<br/>result/analytical/*/] --> LoadAnalytical[加载解析数据]
    CSV2[CSV 文件<br/>result/simulation/*/] --> LoadSimulation[加载模拟数据]
    LoadAnalytical --> Plot[plot/*.py<br/>绘图]
    LoadSimulation --> Plot
    Plot --> PNG[PNG 文件<br/>result/graph/*/]
    
    style CSV1 fill:#f3e5f5
    style CSV2 fill:#f3e5f5
    style LoadAnalytical fill:#c8e6c9
    style LoadSimulation fill:#c8e6c9
    style Plot fill:#ffccbc
    style PNG fill:#e1bee7
```

---

## 模块依赖关系图

```mermaid
graph TD
    Main[main.py<br/>主入口] --> Config[config/loader/loader.py<br/>配置加载]
    Main --> Analytical[analytical/<br/>解析模块]
    Main --> Simulation[simulation/<br/>模拟模块]
    Main --> Plot[plot/<br/>绘图模块]
    
    Analytical --> Formulas[formulas/formulas.py<br/>公式实现]
    Analytical --> Theoretical[theoretical/theoretical.py<br/>理论计算]
    Analytical --> FigAnalysis[figure_analysis/<br/>图表分析]
    
    Theoretical --> Formulas
    
    Simulation --> Core[core/<br/>核心模拟引擎]
    Simulation --> FigSim[figure_simulation/<br/>图表模拟]
    
    Core --> OneShot[one_shot_access.py<br/>单次接入]
    Core --> GroupPaging[group_paging.py<br/>群组寻呼]
    Core --> Metrics[metrics.py<br/>性能指标]
    
    FigSim --> Core
    FigSim --> Analytical
    
    Plot --> Analytical
    Plot --> Simulation
    
    style Main fill:#fff9c4
    style Config fill:#e3f2fd
    style Analytical fill:#ffccbc
    style Simulation fill:#b2dfdb
    style Plot fill:#c5cae9
    style Formulas fill:#f8bbd0
    style Theoretical fill:#f8bbd0
```

---

## 模块依赖关系

### 核心模块

- **config/loader/loader.py**: 所有选项都需要加载配置
- **analytical/formulas/formulas.py**: 提供所有数学公式实现
- **analytical/theoretical/theoretical.py**: 提供多周期理论计算

### 分析模块

- **analytical/figure_analysis/figure1_analysis.py**: Figure 1 计算
- **analytical/figure_analysis/figure2_analysis.py**: Figure 2 计算（依赖 Figure 1）
- **analytical/figure_analysis/figure345_analysis.py**: Figure 3-5 计算

### 模拟模块

- **simulation/core/one_shot_access.py**: 单次接入模拟
- **simulation/core/group_paging.py**: 群组寻呼模拟
- **simulation/core/metrics.py**: 性能指标计算
- **simulation/figure_simulation/figure345_simulation.py**: 模拟协调层

### 绘图模块

- **plot/common.py**: 共用绘图工具
- **plot/figure1.py**: Figure 1 绘图
- **plot/figure2.py**: Figure 2 绘图
- **plot/figure345.py**: Figure 3-5 绘图

---

## 注意事项

1. **Figure 2 依赖 Figure 1**: 选项 2 需要先运行选项 1，或使用选项 4 自动处理依赖
2. **Figure 3-5 模拟需要解析结果**: 选项 5 会尝试加载解析结果计算误差，如果不存在会警告但不影响模拟
3. **绘图选项需要数据**: 选项 6-9 需要先运行对应的解析或模拟选项生成数据
4. **完整流程选项**: 选项 10-13 会自动处理依赖关系，按正确顺序执行
