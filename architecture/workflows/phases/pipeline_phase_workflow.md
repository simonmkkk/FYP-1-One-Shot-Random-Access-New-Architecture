# Pipeline Phase Workflow / 管道階段工作流程

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

