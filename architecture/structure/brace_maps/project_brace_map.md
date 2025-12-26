# Project Brace Map / 項目括號圖

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

## Visual Brace Map Format / 視覺括號圖格式

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

