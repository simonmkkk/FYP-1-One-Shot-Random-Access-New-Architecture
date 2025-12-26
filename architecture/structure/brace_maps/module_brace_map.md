# Module Brace Map / 模組括號圖

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

