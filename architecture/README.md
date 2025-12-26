# Architecture Diagrams / 架構圖表

This directory contains all architecture diagrams organized by fine-grained categories.

本目錄包含按細緻類別組織的所有架構圖表。

## Directory Structure / 目錄結構

```
architecture/
├── structure/                      # 結構相關圖表
│   ├── directory/                   # 目錄相關
│   │   └── directory_tree.md       # 目錄樹狀圖
│   ├── module/                     # 模組相關
│   │   ├── project_structure_diagram.md    # 項目結構圖
│   │   └── module_architecture_diagram.md  # 模組架構圖
│   └── brace_maps/                 # 括號圖
│       ├── project_brace_map.md    # 項目括號圖
│       └── module_brace_map.md     # 模組括號圖
│
├── data_flow/                      # 數據流相關圖表
│   ├── input_output/               # 輸入輸出
│   │   └── data_input_output_diagram.md    # 數據輸入輸出圖
│   └── flow/                       # 數據流
│       └── data_flow_diagram.md    # 數據流圖
│
├── workflows/                      # 工作流程圖表
│   ├── overview/                   # 概覽
│   │   └── complete_pipeline_workflow.md  # 完整管道工作流程
│   ├── phases/                     # 各階段
│   │   ├── analytical_phase_workflow.md    # 解析階段工作流程
│   │   ├── simulation_phase_workflow.md     # 模擬階段工作流程
│   │   ├── plotting_phase_workflow.md      # 繪圖階段工作流程
│   │   └── pipeline_phase_workflow.md      # 管道階段工作流程
│   ├── figures/                    # 各圖表
│   │   ├── figure1_workflow.md     # Figure 1 工作流程
│   │   ├── figure2_workflow.md     # Figure 2 工作流程
│   │   └── figure3_5_workflow.md   # Figure 3-5 工作流程
│   └── brace_maps/                 # 括號圖
│       └── workflow_brace_map.md   # 工作流程括號圖
│
└── formulas/                       # 公式相關圖表
    └── formula_dependency_diagram.md        # 公式依賴圖
```

## Categories / 分類說明

### Structure / 結構

#### Directory / 目錄
- **directory_tree.md**: Complete directory structure of the project / 項目的完整目錄結構

#### Module / 模組
- **project_structure_diagram.md**: Module relationships and dependencies / 模組關係和依賴
- **module_architecture_diagram.md**: Module architecture overview / 模組架構概覽

#### Brace Maps / 括號圖
- **project_brace_map.md**: Hierarchical project structure in brace map format / 項目層次結構括號圖
- **module_brace_map.md**: Module relationships in brace map format / 模組關係括號圖

### Data Flow / 數據流

#### Input-Output / 輸入輸出
- **data_input_output_diagram.md**: Complete data flow from YAML configs to PNG outputs / 從 YAML 配置到 PNG 輸出的完整數據流

#### Flow / 數據流
- **data_flow_diagram.md**: How data moves through the system / 數據在系統中的流動方式

### Workflows / 工作流程

#### Overview / 概覽
- **complete_pipeline_workflow.md**: High-level overview of all workflows / 所有工作流程的高層次概覽

#### Phases / 各階段
- **analytical_phase_workflow.md**: Detailed analytical calculation workflow / 解析計算階段詳細工作流程
- **simulation_phase_workflow.md**: Detailed simulation workflow / 模擬階段詳細工作流程
- **plotting_phase_workflow.md**: Detailed plotting workflow / 繪圖階段詳細工作流程
- **pipeline_phase_workflow.md**: Complete pipeline workflow details / 完整管道工作流程詳情

#### Figures / 各圖表
- **figure1_workflow.md**: Figure 1 specific workflow / Figure 1 特定工作流程
- **figure2_workflow.md**: Figure 2 specific workflow / Figure 2 特定工作流程
- **figure3_5_workflow.md**: Figure 3-5 specific workflow / Figure 3-5 特定工作流程

#### Brace Maps / 括號圖
- **workflow_brace_map.md**: Complete workflow structure in brace map format / 完整工作流程結構括號圖

### Formulas / 公式
- **formula_dependency_diagram.md**: Relationships between the 10 paper formulas / 10 個論文公式之間的關係

## Usage / 使用說明

Each diagram is independent and can be viewed separately. All diagrams use Mermaid syntax and support bilingual labels (English / 中文).

每個圖表都是獨立的，可以單獨查看。所有圖表都使用 Mermaid 語法，並支持雙語標籤（英文 / 中文）。

## Navigation / 導航

- Start with [Complete Pipeline Workflow](workflows/overview/complete_pipeline_workflow.md) for a high-level overview
- Check [Directory Tree](structure/directory/directory_tree.md) to understand the project structure
- Review [Module Architecture](structure/module/module_architecture_diagram.md) for module relationships
- Explore [Workflow Phases](workflows/phases/) for detailed phase workflows
- See [Figure Workflows](workflows/figures/) for figure-specific execution flows

- 從 [完整管道工作流程](workflows/overview/complete_pipeline_workflow.md) 開始了解高層次概覽
- 查看 [目錄樹狀圖](structure/directory/directory_tree.md) 了解項目結構
- 查看 [模組架構圖](structure/module/module_architecture_diagram.md) 了解模組關係
- 探索 [工作流程階段](workflows/phases/) 查看詳細階段工作流程
- 查看 [圖表工作流程](workflows/figures/) 了解圖表特定執行流程

