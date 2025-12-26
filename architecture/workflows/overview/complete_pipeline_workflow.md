# Complete Pipeline Workflow / 完整管道工作流程

This diagram shows the high-level overview of the complete pipeline workflow.

本圖表顯示完整管道工作流程的高層次概覽。

For detailed workflows of each phase, see:
各階段的詳細工作流程請參見：

- [Analytical Phase Workflow](../phases/analytical_phase_workflow.md) - 解析階段工作流程
- [Simulation Phase Workflow](../phases/simulation_phase_workflow.md) - 模擬階段工作流程
- [Plotting Phase Workflow](../phases/plotting_phase_workflow.md) - 繪圖階段工作流程
- [Pipeline Phase Workflow](../phases/pipeline_phase_workflow.md) - 管道階段工作流程

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

