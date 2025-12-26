# Workflow Brace Map / 工作流程括號圖

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

