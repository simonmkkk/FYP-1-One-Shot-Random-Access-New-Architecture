# Architecture Diagrams

This directory contains all architecture diagrams organized by fine-grained categories.

## Directory Structure

```
architecture/
├── structure/                      # Structure-related diagrams
│   ├── directory/                   # Directory-related
│   │   └── directory_tree.md       # Directory tree diagram
│   ├── module/                     # Module-related
│   │   ├── project_structure_diagram.md    # Project structure diagram
│   │   └── module_architecture_diagram.md  # Module architecture diagram
│   └── brace_maps/                 # Brace maps
│       ├── project_brace_map.md    # Project brace map
│       └── module_brace_map.md     # Module brace map
│
├── data_flow/                      # Data flow-related diagrams
│   ├── input_output/               # Input-output
│   │   └── data_input_output_diagram.md    # Data input-output diagram
│   └── flow/                       # Data flow
│       └── data_flow_diagram.md    # Data flow diagram
│
├── workflows/                      # Workflow diagrams
│   ├── overview/                   # Overview
│   │   └── complete_pipeline_workflow.md  # Complete pipeline workflow
│   ├── phases/                     # Phases
│   │   ├── analytical_phase_workflow.md    # Analytical phase workflow
│   │   ├── simulation_phase_workflow.md     # Simulation phase workflow
│   │   ├── plotting_phase_workflow.md      # Plotting phase workflow
│   │   └── pipeline_phase_workflow.md      # Pipeline phase workflow
│   ├── figures/                    # Figures
│   │   ├── figure1_workflow.md     # Figure 1 workflow
│   │   ├── figure2_workflow.md     # Figure 2 workflow
│   │   └── figure3_5_workflow.md   # Figure 3-5 workflow
│   └── brace_maps/                 # Brace maps
│       └── workflow_brace_map.md    # Workflow brace map
│
└── formulas/                       # Formula-related diagrams
    └── formula_dependency_diagram.md        # Formula dependency diagram
```

## Categories

### Structure

#### Directory
- **directory_tree.md**: Complete directory structure of the project

#### Module
- **project_structure_diagram.md**: Module relationships and dependencies
- **module_architecture_diagram.md**: Module architecture overview

#### Brace Maps
- **project_brace_map.md**: Hierarchical project structure in brace map format
- **module_brace_map.md**: Module relationships in brace map format

### Data Flow

#### Input-Output
- **data_input_output_diagram.md**: Complete data flow from YAML configs to PNG outputs

#### Flow
- **data_flow_diagram.md**: How data moves through the system

### Workflows

#### Overview
- **complete_pipeline_workflow.md**: High-level overview of all workflows

#### Phases
- **analytical_phase_workflow.md**: Detailed analytical calculation workflow
- **simulation_phase_workflow.md**: Detailed simulation workflow
- **plotting_phase_workflow.md**: Detailed plotting workflow
- **pipeline_phase_workflow.md**: Complete pipeline workflow details

#### Figures
- **figure1_workflow.md**: Figure 1 specific workflow
- **figure2_workflow.md**: Figure 2 specific workflow
- **figure3_5_workflow.md**: Figure 3-5 specific workflow

#### Brace Maps
- **workflow_brace_map.md**: Complete workflow structure in brace map format

### Formulas
- **formula_dependency_diagram.md**: Relationships between the 10 paper formulas

## Usage

Each diagram is independent and can be viewed separately. All diagrams use Mermaid syntax and support bilingual labels (English / 中文).

## Navigation

- Start with [Complete Pipeline Workflow](workflows/overview/complete_pipeline_workflow.md) for a high-level overview
- Check [Directory Tree](structure/directory/directory_tree.md) to understand the project structure
- Review [Module Architecture](structure/module/module_architecture_diagram.md) for module relationships
- Explore [Workflow Phases](workflows/phases/) for detailed phase workflows
- See [Figure Workflows](workflows/figures/) for figure-specific execution flows
