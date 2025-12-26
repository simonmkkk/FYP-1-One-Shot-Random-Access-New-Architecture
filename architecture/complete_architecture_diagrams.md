# Complete Architecture Diagrams / 完整架構圖表

This document contains all architecture diagrams for the One-Shot Random Access project in a single comprehensive file.

本文檔包含 One-Shot Random Access 項目的所有架構圖表，整合在一個完整的文件中。

---

## Table of Contents / 目錄

1. [Structure Diagrams / 結構圖表](#1-structure-diagrams--結構圖表)
   - [Directory Tree / 目錄樹狀圖](#11-directory-tree--目錄樹狀圖)
   - [Project Structure Diagram / 項目結構圖](#12-project-structure-diagram--項目結構圖)
   - [Module Architecture Diagram / 模組架構圖](#13-module-architecture-diagram--模組架構圖)
   - [Project Brace Map / 項目括號圖](#14-project-brace-map--項目括號圖)
   - [Module Brace Map / 模組括號圖](#15-module-brace-map--模組括號圖)

2. [Data Flow Diagrams / 數據流圖表](#2-data-flow-diagrams--數據流圖表)
   - [Data Input-Output Diagram / 數據輸入輸出圖](#21-data-input-output-diagram--數據輸入輸出圖)
   - [Data Flow Diagram / 數據流圖](#22-data-flow-diagram--數據流圖)

3. [Workflow Diagrams / 工作流程圖表](#3-workflow-diagrams--工作流程圖表)
   - [Complete Pipeline Workflow / 完整管道工作流程](#31-complete-pipeline-workflow--完整管道工作流程)
   - [Analytical Phase Workflow / 解析階段工作流程](#32-analytical-phase-workflow--解析階段工作流程)
   - [Simulation Phase Workflow / 模擬階段工作流程](#33-simulation-phase-workflow--模擬階段工作流程)
   - [Plotting Phase Workflow / 繪圖階段工作流程](#34-plotting-phase-workflow--繪圖階段工作流程)
   - [Pipeline Phase Workflow / 管道階段工作流程](#35-pipeline-phase-workflow--管道階段工作流程)
   - [Figure 1 Workflow / Figure 1 工作流程](#36-figure-1-workflow--figure-1-工作流程)
   - [Figure 2 Workflow / Figure 2 工作流程](#37-figure-2-workflow--figure-2-工作流程)
   - [Figure 3-5 Workflow / Figure 3-5 工作流程](#38-figure-3-5-workflow--figure-3-5-工作流程)
   - [Workflow Brace Map / 工作流程括號圖](#39-workflow-brace-map--工作流程括號圖)

4. [Formula Dependency Diagram / 公式依賴圖](#4-formula-dependency-diagram--公式依賴圖)

---

## 1. Structure Diagrams / 結構圖表

### 1.1 Directory Tree / 目錄樹狀圖

This diagram shows the complete directory structure of the One-Shot Random Access project.

本圖表顯示 One-Shot Random Access 項目的完整目錄結構。

```mermaid
graph TD
    Root["FYP-1-One-Shot-Random-Access-New-Architecture<br/>项目根目录"]
    
    Root --> Main["main.py<br/>主程序入口<br/>CLI + 交互式菜单"]
    Root --> Config["config/<br/>配置文件目录"]
    Root --> Analytical["analytical/<br/>解析计算模块"]
    Root --> Simulation["simulation/<br/>模拟模块"]
    Root --> Plot["plot/<br/>绘图模块"]
    Root --> Docs["docs/<br/>文档目录"]
    Root --> Result["result/<br/>结果输出目录"]
    Root --> ProjectFiles["pyproject.toml<br/>uv.lock<br/>README.md<br/>SIMULATION_OPTIMIZATION.md"]
    
    Config --> ConfigInit["__init__.py"]
    Config --> ConfigLoader["loader.py<br/>配置加载器"]
    Config --> ConfigAnalytical["analytical/<br/>解析配置"]
    Config --> ConfigSimulation["simulation/<br/>模拟配置"]
    
    ConfigAnalytical --> Fig1Yaml["figure1.yaml<br/>Figure 1 配置"]
    ConfigAnalytical --> Fig345Yaml["figure345.yaml<br/>Figure 3-5 配置"]
    
    ConfigSimulation --> SimFig345Yaml["figure345.yaml<br/>Figure 3-5 模拟配置"]
    ConfigSimulation --> SinglePointYaml["single_point.yaml<br/>单点测试配置"]
    
    Analytical --> AnalyticalInit["__init__.py"]
    Analytical --> Formulas["formulas.py<br/>论文公式<br/>Eq. 1-10"]
    Analytical --> Theoretical["theoretical.py<br/>理论计算<br/>多周期迭代"]
    Analytical --> FigureAnalysis["figure_analysis/<br/>各图表解析计算"]
    
    FigureAnalysis --> FigAnalysisInit["__init__.py"]
    FigureAnalysis --> Fig1Analysis["figure1_analysis.py<br/>Figure 1 解析<br/>精确 vs 近似公式"]
    FigureAnalysis --> Fig2Analysis["figure2_analysis.py<br/>Figure 2 解析<br/>误差分析"]
    FigureAnalysis --> Fig345Analysis["figure345_analysis.py<br/>Figure 3-5 合并解析<br/>P_S, T_a, P_C"]
    
    Simulation --> SimulationInit["__init__.py"]
    Simulation --> Core["core/<br/>核心模拟引擎"]
    Simulation --> FigureSimulation["figure_simulation/<br/>各图表模拟"]
    
    Core --> CoreInit["__init__.py"]
    Core --> OneShot["one_shot_access.py<br/>单次接入模拟"]
    Core --> GroupPaging["group_paging.py<br/>群组寻呼模拟<br/>多样本并行"]
    Core --> Metrics["metrics.py<br/>性能指标计算"]
    
    FigureSimulation --> FigSimInit["__init__.py"]
    FigureSimulation --> Fig345Sim["figure345_simulation.py<br/>Figure 3-5 合并模拟"]
    
    Plot --> PlotInit["__init__.py"]
    Plot --> Common["common.py<br/>共用绘图设置"]
    Plot --> Fig1Plot["figure1.py<br/>Figure 1 绘图"]
    Plot --> Fig2Plot["figure2.py<br/>Figure 2 绘图"]
    Plot --> Fig345Plot["figure345.py<br/>Figure 3-5 绘图"]
    
    Result --> ResultAnalytical["analytical/<br/>解析结果 CSV"]
    Result --> ResultSimulation["simulation/<br/>模拟结果 CSV"]
    Result --> ResultGraph["graph/<br/>图表输出 PNG"]
    
    ResultAnalytical --> Fig1Result["figure1/<br/>Figure 1 CSV<br/>按时间戳组织"]
    ResultAnalytical --> Fig2Result["figure2/<br/>Figure 2 CSV<br/>按时间戳组织"]
    ResultAnalytical --> Fig345Result["figure345/<br/>Figure 3-5 CSV<br/>按时间戳组织"]
    
    ResultSimulation --> SimFig345Result["figure345/<br/>Figure 3-5 模拟 CSV<br/>按时间戳组织"]
    
    ResultGraph --> GraphFig1["figure1/<br/>Figure 1 PNG<br/>按时间戳组织"]
    ResultGraph --> GraphFig2["figure2/<br/>Figure 2 PNG<br/>按时间戳组织"]
    ResultGraph --> GraphFig345["figure3-5/<br/>Figure 3-5 PNG<br/>按时间戳组织"]
    
    Docs --> PaperPDF["FYP-Paper-1.pdf<br/>论文PDF"]
    Docs --> PaperMD["Paper.md<br/>论文笔记"]
    
    style Root fill:#e1f5ff
    style Main fill:#fff4e1
    style Analytical fill:#e8f5e9
    style Simulation fill:#fce4ec
    style Plot fill:#f3e5f5
    style Config fill:#fff9c4
    style Result fill:#e0f2f1
    style Docs fill:#f1f8e9
```

---

### 1.2 Project Structure Diagram / 項目結構圖

This diagram shows the relationships and dependencies between modules, showing data flow.

本圖表顯示模組間的關係和依賴，展示數據流向。

```mermaid
graph TB
    subgraph MainModule["main.py / 主程序"]
        CLI["CLI Interface<br/>命令行接口"]
        InteractiveMenu["Interactive Menu<br/>交互式菜单"]
        Pipeline["Pipeline Functions<br/>完整流程函数<br/>run_pipeline_*()"]
    end
    
    subgraph ConfigModule["config / 配置模块"]
        Loader["loader.py<br/>load_config()<br/>配置加载器"]
        YAMLFiles["YAML Config Files<br/>YAML 配置文件<br/>analytical/*.yaml<br/>simulation/*.yaml"]
    end
    
    subgraph AnalyticalModule["analytical / 解析计算模块"]
        Formulas["formulas.py<br/>论文公式<br/>Eq. 1-10<br/>10个公式函数"]
        Theoretical["theoretical.py<br/>theoretical_calculation()<br/>理论计算<br/>多周期迭代"]
        
        subgraph FigAnalysis["figure_analysis / 图表解析"]
            Fig1Analysis["figure1_analysis.py<br/>run_figure1_analysis()<br/>精确 vs 近似公式"]
            Fig2Analysis["figure2_analysis.py<br/>run_figure2_analysis()<br/>误差分析"]
            Fig345Analysis["figure345_analysis.py<br/>run_figure345_analysis()<br/>P_S, T_a, P_C 计算"]
        end
    end
    
    subgraph SimulationModule["simulation / 模拟模块"]
        subgraph CoreSim["core / 核心模拟"]
            OneShot["one_shot_access.py<br/>simulate_one_shot_access()<br/>单次接入模拟"]
            GroupPaging["group_paging.py<br/>simulate_group_paging_multi_samples()<br/>群组寻呼模拟<br/>并行执行"]
            Metrics["metrics.py<br/>calculate_performance_metrics()<br/>性能指标计算"]
        end
        
        Fig345Sim["figure345_simulation.py<br/>run_figure345_simulation()<br/>Figure 3-5 模拟"]
    end
    
    subgraph PlotModule["plot / 绘图模块"]
        Common["common.py<br/>共用绘图设置<br/>extract_n_values_from_data()"]
        Fig1Plot["figure1.py<br/>plot_figure1()<br/>Figure 1 绘图"]
        Fig2Plot["figure2.py<br/>plot_figure2()<br/>Figure 2 绘图"]
        Fig345Plot["figure345.py<br/>plot_figure3/4/5()<br/>Figure 3-5 绘图"]
    end
    
    subgraph Storage["result / 结果存储"]
        CSVAnalytical["analytical/<br/>解析结果 CSV<br/>按时间戳组织"]
        CSVSimulation["simulation/<br/>模拟结果 CSV<br/>按时间戳组织"]
        PNGGraphs["graph/<br/>图表 PNG<br/>按时间戳组织"]
    end
    
    MainModule --> ConfigModule
    MainModule --> AnalyticalModule
    MainModule --> SimulationModule
    MainModule --> PlotModule
    
    ConfigModule --> AnalyticalModule
    ConfigModule --> SimulationModule
    
    AnalyticalModule --> Storage
    SimulationModule --> Storage
    PlotModule --> Storage
    
    Formulas --> FigAnalysis
    Theoretical --> Fig345Analysis
    
    CoreSim --> Fig345Sim
    Fig345Sim --> Storage
    
    CSVAnalytical --> PlotModule
    CSVSimulation --> PlotModule
    
    style MainModule fill:#fff4e1
    style ConfigModule fill:#fff9c4
    style AnalyticalModule fill:#e8f5e9
    style SimulationModule fill:#fce4ec
    style PlotModule fill:#f3e5f5
    style Storage fill:#e0f2f1
```

---

### 1.3 Module Architecture Diagram / 模組架構圖

This diagram shows the module architecture and relationships between Analytical, Simulation, and Plot modules.

本圖表顯示模組架構以及解析計算、模擬和繪圖模組之間的關係。

```mermaid
graph TB
    subgraph MainModule["main.py / 主程式"]
        CLI["CLI Interface<br/>命令行介面"]
        InteractiveMenu["Interactive Menu<br/>互動式選單"]
        Pipeline["Pipeline Functions<br/>完整流程函數"]
    end
    
    subgraph ConfigModule["config / 配置模組"]
        Loader["loader.py<br/>配置載入器"]
        YAMLFiles["YAML Config Files<br/>YAML 配置文件"]
    end
    
    subgraph AnalyticalModule["analytical / 解析計算模組"]
        Formulas["formulas.py<br/>論文公式<br/>Eq. 1-10"]
        Theoretical["theoretical.py<br/>理論計算<br/>多周期迭代"]
        
        subgraph FigAnalysis["figure_analysis / 圖表解析"]
            Fig1Analysis["figure1_analysis.py<br/>精確 vs 近似公式"]
            Fig2Analysis["figure2_analysis.py<br/>誤差分析"]
            Fig345Analysis["figure345_analysis.py<br/>P_S, T_a, P_C 計算"]
        end
    end
    
    subgraph SimulationModule["simulation / 模擬模組"]
        subgraph CoreSim["core / 核心模擬"]
            OneShot["one_shot_access.py<br/>單次接入模擬"]
            GroupPaging["group_paging.py<br/>群組尋呼模擬"]
            Metrics["metrics.py<br/>性能指標計算"]
        end
        
        Fig345Sim["figure345_simulation.py<br/>Figure 3-5 模擬"]
    end
    
    subgraph PlotModule["plot / 繪圖模組"]
        Common["common.py<br/>共用設定"]
        Fig1Plot["figure1.py<br/>Figure 1 繪圖"]
        Fig2Plot["figure2.py<br/>Figure 2 繪圖"]
        Fig345Plot["figure345.py<br/>Figure 3-5 繪圖"]
    end
    
    subgraph Storage["result / 結果存儲"]
        CSVAnalytical["analytical/<br/>解析結果 CSV"]
        CSVSimulation["simulation/<br/>模擬結果 CSV"]
        PNGGraphs["graph/<br/>圖表 PNG"]
    end
    
    MainModule --> ConfigModule
    MainModule --> AnalyticalModule
    MainModule --> SimulationModule
    MainModule --> PlotModule
    
    ConfigModule --> AnalyticalModule
    ConfigModule --> SimulationModule
    
    AnalyticalModule --> Storage
    SimulationModule --> Storage
    PlotModule --> Storage
    
    Formulas --> FigAnalysis
    Theoretical --> Fig345Analysis
    
    CoreSim --> Fig345Sim
    Fig345Sim --> Storage
    
    CSVAnalytical --> PlotModule
    CSVSimulation --> PlotModule
    
    style MainModule fill:#fff4e1
    style ConfigModule fill:#fff9c4
    style AnalyticalModule fill:#e8f5e9
    style SimulationModule fill:#fce4ec
    style PlotModule fill:#f3e5f5
    style Storage fill:#e0f2f1
```

---

### 1.4 Project Brace Map / 項目括號圖

This brace map shows the hierarchical structure of the One-Shot Random Access project.

本括號圖顯示 One-Shot Random Access 項目的層次結構。

```
FYP-1-One-Shot-Random-Access-New-Architecture
├── Main Entry
│   └── main.py (CLI + Interactive Menu)
│
├── Configuration
│   ├── loader.py
│   ├── analytical/
│   │   ├── figure1.yaml
│   │   └── figure345.yaml
│   └── simulation/
│       ├── figure345.yaml
│       └── single_point.yaml
│
├── Analytical Module
│   ├── formulas.py (Eq. 1-10)
│   ├── theoretical.py
│   └── figure_analysis/
│       ├── figure1_analysis.py
│       ├── figure2_analysis.py
│       └── figure345_analysis.py
│
├── Simulation Module
│   ├── core/
│   │   ├── one_shot_access.py
│   │   ├── group_paging.py
│   │   └── metrics.py
│   └── figure_simulation/
│       └── figure345_simulation.py
│
├── Plot Module
│   ├── common.py
│   ├── figure1.py
│   ├── figure2.py
│   └── figure345.py
│
├── Documentation
│   ├── docs/
│   │   ├── FYP-Paper-1.pdf
│   │   └── Paper.md
│   ├── README.md
│   ├── PROJECT_VISUALIZATION.md
│   ├── REPOSITORY_VISUALIZATION.md
│   └── SIMULATION_OPTIMIZATION.md
│
├── Architecture Diagrams
│   ├── structure/
│   │   ├── directory/
│   │   ├── module/
│   │   └── brace_maps/
│   ├── data_flow/
│   │   ├── input_output/
│   │   └── flow/
│   ├── workflows/
│   │   ├── overview/
│   │   ├── phases/
│   │   ├── figures/
│   │   └── brace_maps/
│   └── formulas/
│
└── Output Results
    └── result/
        ├── analytical/
        │   ├── figure1/
        │   ├── figure2/
        │   └── figure345/
        ├── simulation/
        │   └── figure345/
        └── graph/
            ├── figure1/
            ├── figure2/
            └── figure3-5/
```

#### Visual Brace Map Format / 視覺括號圖格式

```
One-Shot Random Access Project
{
    Main Entry
    {
        main.py
    }
    
    Configuration
    {
        loader.py
        analytical/
        {
            figure1.yaml
            figure345.yaml
        }
        simulation/
        {
            figure345.yaml
            single_point.yaml
        }
    }
    
    Analytical Module
    {
        formulas.py (Eq. 1-10)
        theoretical.py
        figure_analysis/
        {
            figure1_analysis.py
            figure2_analysis.py
            figure345_analysis.py
        }
    }
    
    Simulation Module
    {
        core/
        {
            one_shot_access.py
            group_paging.py
            metrics.py
        }
        figure_simulation/
        {
            figure345_simulation.py
        }
    }
    
    Plot Module
    {
        common.py
        figure1.py
        figure2.py
        figure345.py
    }
    
    Documentation
    {
        docs/
        {
            FYP-Paper-1.pdf
            Paper.md
        }
        README.md
        PROJECT_VISUALIZATION.md
        REPOSITORY_VISUALIZATION.md
        SIMULATION_OPTIMIZATION.md
    }
    
    Architecture Diagrams
    {
        structure/
        {
            directory/
            module/
            brace_maps/
        }
        data_flow/
        {
            input_output/
            flow/
        }
        workflows/
        {
            overview/
            phases/
            figures/
            brace_maps/
        }
        formulas/
    }
    
    Output Results
    {
        result/
        {
            analytical/
            {
                figure1/
                figure2/
                figure345/
            }
            simulation/
            {
                figure345/
            }
            graph/
            {
                figure1/
                figure2/
                figure3-5/
            }
        }
    }
}
```

---

### 1.5 Module Brace Map / 模組括號圖

This brace map shows the module relationships and data flow in the project.

本括號圖顯示項目中的模組關係和數據流。

```
One-Shot Random Access System
{
    Main Module (main.py)
    {
        CLI Interface
        Interactive Menu
        Pipeline Functions
    }
    
    Configuration Module
    {
        loader.py
        {
            load_config()
        }
        YAML Files
        {
            analytical/
            {
                figure1.yaml
                figure345.yaml
            }
            simulation/
            {
                figure345.yaml
                single_point.yaml
            }
        }
    }
    
    Analytical Module
    {
        Core Components
        {
            formulas.py
            {
                Eq. 1-10
                {
                    Single Cycle Formulas (Eq. 1-5)
                    Multi-Cycle Formulas (Eq. 6-7)
                    Performance Metrics (Eq. 8-10)
                }
            }
            theoretical.py
            {
                theoretical_calculation()
            }
        }
        Figure Analysis
        {
            figure1_analysis.py
            {
                Exact vs Approximate Formulas
            }
            figure2_analysis.py
            {
                Error Analysis
            }
            figure345_analysis.py
            {
                P_S, T_a, P_C Calculation
            }
        }
        Output
        {
            CSV Files
            {
                figure1/
                figure2/
                figure345/
            }
        }
    }
    
    Simulation Module
    {
        Core Engine
        {
            one_shot_access.py
            {
                Single AC Cycle Simulation
            }
            group_paging.py
            {
                Multi-Sample Parallel Simulation
            }
            metrics.py
            {
                Performance Metrics Calculation
                Mean + Confidence Interval
            }
        }
        Figure Simulation
        {
            figure345_simulation.py
            {
                Monte Carlo Simulation
                Error Calculation
            }
        }
        Output
        {
            CSV Files
            {
                figure345/
                {
                    P_S, T_a, P_C
                    Error Data
                }
            }
        }
    }
    
    Plot Module
    {
        Common Utilities
        {
            common.py
            {
                extract_n_values_from_data()
            }
        }
        Figure Plotters
        {
            figure1.py
            {
                plot_figure1()
            }
            figure2.py
            {
                plot_figure2()
            }
            figure345.py
            {
                plot_figure3()
                plot_figure4()
                plot_figure5()
            }
        }
        Output
        {
            PNG Graphs
            {
                figure1/
                figure2/
                figure3-5/
            }
        }
    }
    
    Data Flow
    {
        Input
        {
            YAML Config Files
        }
        Processing
        {
            Analytical Calculations
            Simulation (Monte Carlo)
            Error Calculation
        }
        Storage
        {
            CSV Files (Analytical Results)
            CSV Files (Simulation Results)
        }
        Visualization
        {
            Load CSV Data
            Generate PNG Graphs
        }
        Output
        {
            PNG Graphs
        }
    }
}
```

---

## 2. Data Flow Diagrams / 數據流圖表

### 2.1 Data Input-Output Diagram / 數據輸入輸出圖

This diagram shows the complete data flow from YAML configs to final PNG graphs.

本圖表顯示從 YAML 配置到最終 PNG 圖表的完整數據流。

```mermaid
flowchart LR
    subgraph Input["Input / 输入"]
        YAMLConfig["YAML Config Files<br/>YAML 配置文件<br/>config/analytical/figure1.yaml<br/>config/analytical/figure345.yaml<br/>config/simulation/figure345.yaml"]
    end
    
    subgraph Processing["Processing / 处理"]
        subgraph Analytical["Analytical / 解析计算"]
            LoadConfig1["load_config()<br/>加载配置"]
            Formulas1["formulas.py<br/>Eq. 1-10<br/>论文公式<br/>精确公式 + 近似公式"]
            Theoretical1["theoretical.py<br/>theoretical_calculation()<br/>多周期迭代计算<br/>I_max 个 AC 周期"]
            FigAnalysis1["figure_analysis/<br/>各图表解析计算<br/>并行计算优化"]
        end
        
        subgraph Simulation["Simulation / 模拟"]
            LoadConfig2["load_config()<br/>加载配置"]
            OneShotSim["one_shot_access.py<br/>单次接入模拟<br/>单个 AC 周期"]
            GroupPagingSim["group_paging.py<br/>群组寻呼模拟<br/>多 AC 周期 + 多样本<br/>并行执行优化"]
            MetricsSim["metrics.py<br/>性能指标计算<br/>均值 + 置信区间"]
            ErrorCalc["Error Calculation<br/>误差计算<br/>|analytical - sim| / |analytical|"]
        end
    end
    
    subgraph Storage["Storage / 存储"]
        CSVAnalytical["CSV Files<br/>CSV 文件<br/>result/analytical/figure1/*.csv<br/>result/analytical/figure2/*.csv<br/>result/analytical/figure345/*.csv"]
        CSVSimulation["CSV Files<br/>CSV 文件<br/>result/simulation/figure345/*.csv<br/>包含误差数据"]
    end
    
    subgraph Visualization["Visualization / 可视化"]
        LoadCSV["Load CSV Data<br/>载入 CSV 数据<br/>load_figure*_results()"]
        PlotFunctions["plot/*.py<br/>绘图函数<br/>plot_figure1/2/3/4/5()"]
        GeneratePNG["Generate PNG<br/>生成 PNG 图表<br/>matplotlib.savefig()"]
    end
    
    subgraph Output["Output / 输出"]
        PNGFiles["PNG Graphs<br/>PNG 图表<br/>result/graph/figure1/*.png<br/>result/graph/figure2/*.png<br/>result/graph/figure3-5/*.png"]
    end
    
    YAMLConfig --> LoadConfig1
    YAMLConfig --> LoadConfig2
    
    LoadConfig1 --> Formulas1
    Formulas1 --> Theoretical1
    Theoretical1 --> FigAnalysis1
    FigAnalysis1 --> CSVAnalytical
    
    LoadConfig2 --> OneShotSim
    OneShotSim --> GroupPagingSim
    GroupPagingSim --> MetricsSim
    MetricsSim --> ErrorCalc
    ErrorCalc --> CSVSimulation
    
    CSVAnalytical --> LoadCSV
    CSVSimulation --> LoadCSV
    LoadCSV --> PlotFunctions
    PlotFunctions --> GeneratePNG
    GeneratePNG --> PNGFiles
    
    CSVAnalytical -.->|"Read for Error Calculation<br/>读取用于误差计算"| ErrorCalc
    
    style Input fill:#e3f2fd
    style Processing fill:#fff9c4
    style Storage fill:#e8f5e9
    style Visualization fill:#f3e5f5
    style Output fill:#e0f2f1
```

---

### 2.2 Data Flow Diagram / 數據流圖

This diagram shows how data moves from YAML configs through processing to final PNG outputs.

本圖表顯示數據如何從 YAML 配置通過處理流向最終的 PNG 輸出。

```mermaid
flowchart LR
    subgraph Input["Input / 輸入"]
        YAMLConfig["YAML Config Files<br/>YAML 配置文件<br/>config/analytical/*.yaml<br/>config/simulation/*.yaml"]
    end
    
    subgraph Processing["Processing / 處理"]
        subgraph Analytical["Analytical / 解析計算"]
            LoadConfig1["load_config()<br/>載入配置"]
            Formulas1["formulas.py<br/>Eq. 1-10<br/>論文公式"]
            Theoretical1["theoretical.py<br/>多周期迭代計算"]
            FigAnalysis1["figure_analysis/<br/>各圖表解析計算"]
        end
        
        subgraph Simulation["Simulation / 模擬"]
            LoadConfig2["load_config()<br/>載入配置"]
            OneShotSim["one_shot_access.py<br/>單次接入模擬"]
            GroupPagingSim["group_paging.py<br/>群組尋呼模擬"]
            MetricsSim["metrics.py<br/>性能指標計算"]
            ErrorCalc["Error Calculation<br/>誤差計算<br/>|analytical - sim| / |analytical|"]
        end
    end
    
    subgraph Storage["Storage / 存儲"]
        CSVAnalytical["CSV Files<br/>CSV 文件<br/>result/analytical/*.csv"]
        CSVSimulation["CSV Files<br/>CSV 文件<br/>result/simulation/*.csv"]
    end
    
    subgraph Visualization["Visualization / 可視化"]
        LoadCSV["Load CSV Data<br/>載入 CSV 數據"]
        PlotFunctions["plot/*.py<br/>繪圖函數"]
        GeneratePNG["Generate PNG<br/>生成 PNG 圖表"]
    end
    
    subgraph Output["Output / 輸出"]
        PNGFiles["PNG Graphs<br/>PNG 圖表<br/>result/graph/*.png"]
    end
    
    YAMLConfig --> LoadConfig1
    YAMLConfig --> LoadConfig2
    
    LoadConfig1 --> Formulas1
    Formulas1 --> Theoretical1
    Theoretical1 --> FigAnalysis1
    FigAnalysis1 --> CSVAnalytical
    
    LoadConfig2 --> OneShotSim
    OneShotSim --> GroupPagingSim
    GroupPagingSim --> MetricsSim
    MetricsSim --> ErrorCalc
    ErrorCalc --> CSVSimulation
    
    CSVAnalytical --> LoadCSV
    CSVSimulation --> LoadCSV
    LoadCSV --> PlotFunctions
    PlotFunctions --> GeneratePNG
    GeneratePNG --> PNGFiles
    
    CSVAnalytical -.->|"Read for Error Calculation<br/>讀取用於誤差計算"| ErrorCalc
    
    style Input fill:#e3f2fd
    style Processing fill:#fff9c4
    style Storage fill:#e8f5e9
    style Visualization fill:#f3e5f5
    style Output fill:#e0f2f1
```

---

## 3. Workflow Diagrams / 工作流程圖表

### 3.1 Complete Pipeline Workflow / 完整管道工作流程

This diagram shows the high-level overview of the complete pipeline workflow.

本圖表顯示完整管道工作流程的高層次概覽。

```mermaid
flowchart TD
    Start([User Starts / 用戶開始]) --> Menu{Interactive Menu /<br/>互動式選單}
    
    Menu -->|"Option 1-4 / 選項 1-4"| Analytical[Analytical Calculations /<br/>解析計算]
    Menu -->|"Option 5 / 選項 5"| Simulation[Simulation /<br/>模擬]
    Menu -->|"Option 6-9 / 選項 6-9"| Plotting[Plotting /<br/>繪圖]
    Menu -->|"Option 10-13 / 選項 10-13"| Pipeline[Complete Pipeline /<br/>完整管道]
    
    Analytical --> AnalyticalOutput[CSV Files /<br/>CSV 文件]
    Simulation --> SimulationOutput[CSV Files /<br/>CSV 文件]
    Plotting --> PlottingOutput[PNG Graphs /<br/>PNG 圖表]
    Pipeline --> PipelineOutput[Complete Results /<br/>完整結果]
    
    AnalyticalOutput --> End([Complete / 完成])
    SimulationOutput --> End
    PlottingOutput --> End
    PipelineOutput --> End
    
    style Start fill:#e3f2fd
    style Menu fill:#fff9c4
    style Analytical fill:#e8f5e9
    style Simulation fill:#fce4ec
    style Plotting fill:#f3e5f5
    style Pipeline fill:#fff4e1
    style End fill:#e0f2f1
```

---

### 3.2 Analytical Phase Workflow / 解析階段工作流程

This diagram shows the detailed workflow for the analytical calculation phase.

本圖表顯示解析計算階段的詳細工作流程。

```mermaid
flowchart TD
    Start([Analytical Calculations / 解析計算]) --> Fig1[Figure 1 Analysis /<br/>Figure 1 解析<br/>精確 vs 近似公式]
    Start --> Fig2[Figure 2 Analysis /<br/>Figure 2 解析<br/>誤差分析]
    Start --> Fig345[Figure 3-5 Analysis /<br/>Figure 3-5 解析<br/>P_S, T_a, P_C]
    
    Fig1 --> CSV1[Save to CSV /<br/>保存到 CSV<br/>result/analytical/figure1/]
    Fig2 --> CSV2[Save to CSV /<br/>保存到 CSV<br/>result/analytical/figure2/]
    Fig345 --> CSV3[Save to CSV /<br/>保存到 CSV<br/>result/analytical/figure345/]
    
    CSV1 --> End([Complete / 完成])
    CSV2 --> End
    CSV3 --> End
    
    style Start fill:#e8f5e9
    style Fig1 fill:#c8e6c9
    style Fig2 fill:#c8e6c9
    style Fig345 fill:#c8e6c9
    style CSV1 fill:#a5d6a7
    style CSV2 fill:#a5d6a7
    style CSV3 fill:#a5d6a7
    style End fill:#e0f2f1
```

---

### 3.3 Simulation Phase Workflow / 模擬階段工作流程

This diagram shows the detailed workflow for the simulation phase.

本圖表顯示模擬階段的詳細工作流程。

```mermaid
flowchart TD
    Start([Simulation / 模擬]) --> Fig345Sim[Figure 3-5 Simulation /<br/>Figure 3-5 模擬<br/>Monte Carlo]
    
    Fig345Sim --> ErrorCalc["Calculate Error /<br/>計算誤差<br/>|analytical - sim| / |analytical|"]
    
    ErrorCalc --> CSV4[Save to CSV /<br/>保存到 CSV<br/>result/simulation/figure345/]
    
    CSV4 --> End([Complete / 完成])
    
    style Start fill:#fce4ec
    style Fig345Sim fill:#f8bbd0
    style ErrorCalc fill:#f48fb1
    style CSV4 fill:#f06292
    style End fill:#e0f2f1
```

---

### 3.4 Plotting Phase Workflow / 繪圖階段工作流程

This diagram shows the detailed workflow for the plotting phase.

本圖表顯示繪圖階段的詳細工作流程。

```mermaid
flowchart TD
    Start([Plotting / 繪圖]) --> LoadCSV[Load CSV Data /<br/>載入 CSV 數據]
    
    LoadCSV --> Plot1[Plot Figure 1 /<br/>繪製 Figure 1]
    LoadCSV --> Plot2[Plot Figure 2 /<br/>繪製 Figure 2]
    LoadCSV --> Plot345[Plot Figure 3-5 /<br/>繪製 Figure 3-5]
    
    Plot1 --> PNG1[Save PNG /<br/>保存 PNG<br/>result/graph/figure1/]
    Plot2 --> PNG2[Save PNG /<br/>保存 PNG<br/>result/graph/figure2/]
    Plot345 --> PNG345[Save PNG /<br/>保存 PNG<br/>result/graph/figure3-5/]
    
    PNG1 --> End([Complete / 完成])
    PNG2 --> End
    PNG345 --> End
    
    style Start fill:#f3e5f5
    style LoadCSV fill:#e1bee7
    style Plot1 fill:#ce93d8
    style Plot2 fill:#ce93d8
    style Plot345 fill:#ce93d8
    style PNG1 fill:#ba68c8
    style PNG2 fill:#ba68c8
    style PNG345 fill:#ba68c8
    style End fill:#e0f2f1
```

---

### 3.5 Pipeline Phase Workflow / 管道階段工作流程

This diagram shows the detailed workflow for the complete pipeline phase, which combines analytical, simulation, and plotting phases.

本圖表顯示完整管道階段的詳細工作流程，該階段結合了解析、模擬和繪圖階段。

```mermaid
flowchart TD
    Start([Complete Pipeline / 完整管道]) --> PipelineFig1[Figure 1 Pipeline /<br/>Figure 1 管道<br/>Analytical → Plot]
    Start --> PipelineFig2[Figure 2 Pipeline /<br/>Figure 2 管道<br/>Analytical → Plot]
    Start --> PipelineFig345[Figure 3-5 Pipeline /<br/>Figure 3-5 管道<br/>Analytical → Simulation → Plot]
    
    PipelineFig1 --> Fig1Analysis[Figure 1 Analysis /<br/>Figure 1 解析]
    PipelineFig1 --> Fig1Plot[Plot Figure 1 /<br/>繪製 Figure 1]
    Fig1Analysis --> Fig1Plot
    
    PipelineFig2 --> Fig2Analysis[Figure 2 Analysis /<br/>Figure 2 解析]
    PipelineFig2 --> Fig2Plot[Plot Figure 2 /<br/>繪製 Figure 2]
    Fig2Analysis --> Fig2Plot
    
    PipelineFig345 --> Fig345Analysis[Figure 3-5 Analysis /<br/>Figure 3-5 解析]
    PipelineFig345 --> Fig345Sim[Figure 3-5 Simulation /<br/>Figure 3-5 模擬]
    PipelineFig345 --> Fig345Plot[Plot Figure 3-5 /<br/>繪製 Figure 3-5]
    Fig345Analysis --> Fig345Plot
    Fig345Sim --> Fig345Plot
    
    Fig1Plot --> End([Complete / 完成])
    Fig2Plot --> End
    Fig345Plot --> End
    
    style Start fill:#fff4e1
    style PipelineFig1 fill:#ffe0b2
    style PipelineFig2 fill:#ffe0b2
    style PipelineFig345 fill:#ffe0b2
    style Fig1Analysis fill:#ffcc80
    style Fig2Analysis fill:#ffcc80
    style Fig345Analysis fill:#ffcc80
    style Fig345Sim fill:#ffb74d
    style Fig1Plot fill:#ffa726
    style Fig2Plot fill:#ffa726
    style Fig345Plot fill:#ffa726
    style End fill:#e0f2f1
```

---

### 3.6 Figure 1 Workflow / Figure 1 工作流程

This diagram shows the detailed execution flow for Figure 1 analysis and plotting.

本圖表顯示 Figure 1 分析和繪圖的詳細執行流程。

```mermaid
sequenceDiagram
    participant User as User / 用户
    participant Main as main.py
    participant Config as config/loader.py
    participant Fig1Analysis as figure1_analysis.py
    participant Formulas as formulas.py
    participant CSV as CSV File / CSV 文件
    participant Plot as plot/figure1.py
    participant PNG as PNG Graph / PNG 图表
    
    User->>Main: Run Figure 1 / 运行 Figure 1
    Main->>Config: load_config('analytical', 'figure1')<br/>加载配置
    Config->>Config: Read figure1.yaml<br/>读取配置文件
    Config-->>Main: Return config / 返回配置
    
    Main->>Fig1Analysis: run_figure1_analysis(config)<br/>运行 Figure 1 解析
    Fig1Analysis->>Formulas: paper_formula_3_success_raos_exact()<br/>精确成功公式 Eq. 3
    Formulas-->>Fig1Analysis: N_S values / N_S 值
    Fig1Analysis->>Formulas: paper_formula_2_collision_raos_exact()<br/>精确碰撞公式 Eq. 2
    Formulas-->>Fig1Analysis: N_C values / N_C 值
    Fig1Analysis->>Formulas: paper_formula_4_success_approx()<br/>近似成功公式 Eq. 4
    Formulas-->>Fig1Analysis: Approx N_S / 近似 N_S
    Fig1Analysis->>Formulas: paper_formula_5_collision_approx()<br/>近似碰撞公式 Eq. 5
    Formulas-->>Fig1Analysis: Approx N_C / 近似 N_C
    
    Fig1Analysis->>CSV: Save results / 保存结果<br/>result/analytical/figure1/*.csv
    CSV-->>Main: Complete / 完成
    
    Main->>Plot: plot_figure1(data)<br/>绘制 Figure 1
    Plot->>CSV: Load data / 载入数据
    CSV-->>Plot: Return data / 返回数据
    Plot->>PNG: Save figure / 保存图表<br/>result/graph/figure1/figure1.png
    PNG-->>User: Display / 显示
```

---

### 3.7 Figure 2 Workflow / Figure 2 工作流程

This diagram shows the detailed execution flow for Figure 2 error analysis and plotting.

本圖表顯示 Figure 2 誤差分析和繪圖的詳細執行流程。

```mermaid
sequenceDiagram
    participant User as User / 用户
    participant Main as main.py
    participant Config as config/loader.py
    participant Fig2Analysis as figure2_analysis.py
    participant Fig1Analysis as figure1_analysis.py
    participant CSV as CSV File / CSV 文件
    participant Plot as plot/figure2.py
    participant PNG as PNG Graph / PNG 图表
    
    User->>Main: Run Figure 2 / 运行 Figure 2
    Main->>Config: load_config('analytical', 'figure1')<br/>加载配置（使用 Figure 1 配置）
    Config-->>Main: Return config / 返回配置
    
    Main->>Fig2Analysis: run_figure2_analysis(config)<br/>运行 Figure 2 解析
    Fig2Analysis->>Fig1Analysis: run_figure1_analysis()<br/>先运行 Figure 1（不保存）
    Fig1Analysis-->>Fig2Analysis: Return data / 返回数据
    
    Fig2Analysis->>Fig2Analysis: Calculate error / 计算误差<br/>error = |analytical - approx| / |analytical|
    Fig2Analysis->>CSV: Save error results / 保存误差结果<br/>result/analytical/figure2/*.csv
    CSV-->>Main: Complete / 完成
    
    Main->>Plot: plot_figure2(data)<br/>绘制 Figure 2
    Plot->>CSV: Load data / 载入数据
    CSV-->>Plot: Return data / 返回数据
    Plot->>PNG: Save figure / 保存图表<br/>result/graph/figure2/figure2.png
    PNG-->>User: Display / 显示
```

---

### 3.8 Figure 3-5 Workflow / Figure 3-5 工作流程

This diagram shows the detailed execution flow for Figure 3-5 analysis, simulation, and plotting.

本圖表顯示 Figure 3-5 分析、模擬和繪圖的詳細執行流程。

```mermaid
sequenceDiagram
    participant User as User / 用户
    participant Main as main.py
    participant Config as config/loader.py
    participant Fig345Analysis as figure345_analysis.py
    participant Theoretical as theoretical.py
    participant Formulas as formulas.py
    participant CSVAnalytical as Analytical CSV / 解析 CSV
    participant Fig345Sim as figure345_simulation.py
    participant GroupPaging as group_paging.py
    participant Metrics as metrics.py
    participant CSVSimulation as Simulation CSV / 模拟 CSV
    participant Plot as plot/figure345.py
    participant PNG as PNG Graphs / PNG 图表
    
    Note over User,PNG: Analytical Phase / 解析阶段
    User->>Main: Run Figure 3-5 Analytical / 运行 Figure 3-5 解析
    Main->>Config: load_config('analytical', 'figure345')<br/>加载配置
    Config-->>Main: Return config / 返回配置
    
    Main->>Fig345Analysis: run_figure345_analysis(config)<br/>运行 Figure 3-5 解析
    Fig345Analysis->>Theoretical: theoretical_calculation(M, N, I_max)<br/>理论计算
    Theoretical->>Formulas: paper_formula_6_success_per_cycle()<br/>Eq. 6 迭代
    Theoretical->>Formulas: paper_formula_7_next_contending_devices()<br/>Eq. 7 迭代
    Theoretical->>Formulas: paper_formula_8_access_success_probability()<br/>Eq. 8 → P_S
    Theoretical->>Formulas: paper_formula_9_mean_access_delay()<br/>Eq. 9 → T_a
    Theoretical->>Formulas: paper_formula_10_collision_probability()<br/>Eq. 10 → P_C
    Formulas-->>Theoretical: Return values / 返回值
    Theoretical-->>Fig345Analysis: P_S, T_a, P_C
    Fig345Analysis->>CSVAnalytical: Save results / 保存结果<br/>result/analytical/figure345/*.csv
    
    Note over User,PNG: Simulation Phase / 模拟阶段
    User->>Main: Run Figure 3-5 Simulation / 运行 Figure 3-5 模拟
    Main->>Config: load_config('simulation', 'figure345')<br/>加载配置
    Config-->>Main: Return config / 返回配置
    
    Main->>Fig345Sim: run_figure345_simulation(config)<br/>运行 Figure 3-5 模拟
    Fig345Sim->>GroupPaging: simulate_group_paging_multi_samples()<br/>群组寻呼多样本模拟
    GroupPaging->>GroupPaging: Parallel simulation / 并行模拟<br/>num_samples times / num_samples 次
    GroupPaging-->>Fig345Sim: Simulation results / 模拟结果
    Fig345Sim->>Metrics: calculate_performance_metrics()<br/>计算性能指标
    Metrics-->>Fig345Sim: P_S, T_a, P_C (mean + CI) / 均值 + 置信区间
    
    Fig345Sim->>CSVAnalytical: Load analytical results / 载入解析结果
    CSVAnalytical-->>Fig345Sim: Return analytical data / 返回解析数据
    Fig345Sim->>Fig345Sim: Calculate approximation error / 计算近似误差<br/>|analytical - sim| / |analytical|
    Fig345Sim->>CSVSimulation: Save results + errors / 保存结果 + 误差<br/>result/simulation/figure345/*.csv
    
    Note over User,PNG: Plotting Phase / 绘图阶段
    User->>Main: Run Figure 3-5 Plot / 运行 Figure 3-5 绘图
    Main->>Plot: plot_figure3/4/5()<br/>绘制 Figure 3/4/5
    Plot->>CSVAnalytical: Load analytical data / 载入解析数据
    CSVAnalytical-->>Plot: Return analytical data / 返回解析数据
    Plot->>CSVSimulation: Load simulation data / 载入模拟数据
    CSVSimulation-->>Plot: Return simulation data + errors / 返回模拟数据 + 误差
    Plot->>PNG: Save figures / 保存图表<br/>result/graph/figure3-5/*.png
    PNG-->>User: Display / 显示
```

---

### 3.9 Workflow Brace Map / 工作流程括號圖

This brace map shows the complete workflow structure of the project.

本括號圖顯示項目的完整工作流程結構。

```
Complete Workflow System
{
    User Interaction
    {
        Interactive Menu
        {
            Option 1-4: Analytical Calculations
            Option 5: Simulation
            Option 6-9: Plotting
            Option 10-13: Complete Pipeline
        }
    }
    
    Analytical Phase
    {
        Figure 1 Analysis
        {
            Load Config (figure1.yaml)
            Calculate
            {
                Exact Formulas (Eq. 2, 3)
                Approximate Formulas (Eq. 4, 5)
            }
            Save to CSV
            {
                result/analytical/figure1/
            }
        }
        Figure 2 Analysis
        {
            Load Config (figure1.yaml)
            Run Figure 1 (internal)
            Calculate Error
            {
                |analytical - approx| / |analytical|
            }
            Save to CSV
            {
                result/analytical/figure2/
            }
        }
        Figure 3-5 Analysis
        {
            Load Config (figure345.yaml)
            Theoretical Calculation
            {
                Multi-Cycle Iteration (Eq. 6, 7)
                Performance Metrics
                {
                    P_S (Eq. 8)
                    T_a (Eq. 9)
                    P_C (Eq. 10)
                }
            }
            Save to CSV
            {
                result/analytical/figure345/
            }
        }
    }
    
    Simulation Phase
    {
        Figure 3-5 Simulation
        {
            Load Config (figure345.yaml)
            Group Paging Simulation
            {
                Parallel Multi-Sample
                {
                    num_samples iterations
                }
            }
            Calculate Metrics
            {
                Mean + Confidence Interval
            }
            Calculate Error
            {
                |analytical - sim| / |analytical|
            }
            Save to CSV
            {
                result/simulation/figure345/
            }
        }
    }
    
    Plotting Phase
    {
        Load CSV Data
        {
            From analytical/
            From simulation/
        }
        Plot Figures
        {
            Figure 1
            {
                plot_figure1()
                Save PNG
                {
                    result/graph/figure1/
                }
            }
            Figure 2
            {
                plot_figure2()
                Save PNG
                {
                    result/graph/figure2/
                }
            }
            Figure 3-5
            {
                plot_figure3()
                plot_figure4()
                plot_figure5()
                Save PNG
                {
                    result/graph/figure3-5/
                }
            }
        }
    }
    
    Complete Pipeline
    {
        Figure 1 Pipeline
        {
            Analytical Phase
            Plotting Phase
        }
        Figure 2 Pipeline
        {
            Analytical Phase
            Plotting Phase
        }
        Figure 3-5 Pipeline
        {
            Analytical Phase
            Simulation Phase
            Plotting Phase
        }
    }
}
```

---

## 4. Formula Dependency Diagram / 公式依賴圖

This diagram shows the dependency relationships between the 10 paper formulas and their correspondence with figures.

本圖表顯示 10 個論文公式之間的依賴關係及其與圖表的對應。

```mermaid
graph TB
    subgraph SingleCycle["Single Cycle Formulas / 单周期公式"]
        Eq1["Eq. 1<br/>paper_formula_1_pk_probability<br/>k 个碰撞 RAO 的概率<br/>P_k 概率计算<br/>基础组合公式"]
        
        Eq2["Eq. 2<br/>paper_formula_2_collision_raos_exact<br/>期望碰撞 RAO 数（精确）<br/>N_C 精确值<br/>基于 Eq. 1"]
        
        Eq3["Eq. 3<br/>paper_formula_3_success_raos_exact<br/>期望成功 RAO 数（精确）<br/>N_S 精确值<br/>基于 Eq. 1"]
        
        Eq4["Eq. 4<br/>paper_formula_4_success_approx<br/>成功 RAO 近似公式<br/>N_S ≈ M·e^(-M/N1)<br/>独立近似公式"]
        
        Eq5["Eq. 5<br/>paper_formula_5_collision_approx<br/>碰撞 RAO 近似公式<br/>N_C ≈ N1·(1 - e^(-M/N1)·(1 + M/N1))<br/>独立近似公式"]
    end
    
    subgraph MultiCycle["Multi-Cycle Iteration Formulas / 多周期迭代公式"]
        Eq6["Eq. 6<br/>paper_formula_6_success_per_cycle<br/>第 i 个 AC 成功设备数<br/>N_S,i = K_i·e^(-K_i/N_i)<br/>基于 Eq. 4 的迭代版本"]
        
        Eq7["Eq. 7<br/>paper_formula_7_next_contending_devices<br/>下一个 AC 竞争设备数<br/>K_i+1 = K_i·(1 - e^(-K_i/N_i))<br/>基于 Eq. 6"]
    end
    
    subgraph Performance["Performance Metrics / 性能指标公式"]
        Eq8["Eq. 8<br/>paper_formula_8_access_success_probability<br/>接入成功概率<br/>P_S = Σ N_S,i / M<br/>基于 Eq. 6 的累积"]
        
        Eq9["Eq. 9<br/>paper_formula_9_mean_access_delay<br/>平均接入延迟<br/>T_a = Σ(i·N_S,i) / Σ N_S,i<br/>基于 Eq. 6 的加权平均"]
        
        Eq10["Eq. 10<br/>paper_formula_10_collision_probability<br/>碰撞概率<br/>P_C = Σ N_C,i / (I_max × N)<br/>基于 Eq. 5 的累积"]
    end
    
    subgraph Figures["Figures / 图表"]
        Fig1["Figure 1<br/>N_S, N_C<br/>精确 vs 近似<br/>使用 Eq. 2, 3, 4, 5"]
        Fig2["Figure 2<br/>误差分析<br/>精确 vs 近似<br/>使用 Eq. 2, 3, 4, 5"]
        Fig3["Figure 3<br/>P_S<br/>成功概率<br/>使用 Eq. 8"]
        Fig4["Figure 4<br/>T_a<br/>平均延迟<br/>使用 Eq. 9"]
        Fig5["Figure 5<br/>P_C<br/>碰撞概率<br/>使用 Eq. 10"]
    end
    
    Eq1 --> Eq2
    Eq1 --> Eq3
    
    Eq2 --> Fig1
    Eq3 --> Fig1
    Eq4 --> Fig1
    Eq5 --> Fig1
    
    Eq2 --> Fig2
    Eq3 --> Fig2
    Eq4 --> Fig2
    Eq5 --> Fig2
    
    Eq4 --> Eq6
    Eq5 --> Eq10
    
    Eq6 --> Eq7
    Eq7 --> Eq6
    
    Eq6 --> Eq8
    Eq6 --> Eq9
    Eq6 --> Eq10
    
    Eq7 --> Eq8
    Eq7 --> Eq9
    Eq7 --> Eq10
    
    Eq8 --> Fig3
    Eq9 --> Fig4
    Eq10 --> Fig5
    
    style SingleCycle fill:#e8f5e9
    style MultiCycle fill:#fff9c4
    style Performance fill:#fce4ec
    style Figures fill:#f3e5f5
```

---

## Summary / 總結

This comprehensive document contains all architecture diagrams for the One-Shot Random Access project, including:

本文檔包含 One-Shot Random Access 項目的所有架構圖表，包括：

1. **Structure Diagrams / 結構圖表**: Directory tree, project structure, module architecture, and brace maps
2. **Data Flow Diagrams / 數據流圖表**: Input-output flow and data movement through the system
3. **Workflow Diagrams / 工作流程圖表**: Complete pipeline, phase workflows, figure-specific workflows, and brace maps
4. **Formula Dependency Diagram / 公式依賴圖**: Relationships between the 10 paper formulas

All diagrams use bilingual labels (English / 中文) for better understanding and are organized in a logical structure for easy navigation.

所有圖表都使用雙語標籤（英文 / 中文）以便更好地理解，並以邏輯結構組織，便於導航。

