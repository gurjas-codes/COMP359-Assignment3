# COMP359 Assignment 3 - Linear Programming Simplex Visualization

## Project Overview

This project demonstrates the Simplex algorithm for solving linear programming problems through multiple visualization approaches. The team implemented three distinct methods to explore LP solutions from 2D interactive visualization to high-dimensional problem analysis.

### Topics Covered

* **2D Simplex Visualization** - Step-by-step visualization of the Simplex algorithm on a 2-variable problem
* **Library Implementation** - Solving a 5+ constraint LP problem using PuLP library
* **Higher Dimensions** - Exploring the `long15.mps` network LP benchmark and visualizing high-dimensional solutions

---

## Team Members

| Member  | Role                             | Contribution                                                              |
| ------- | -------------------------------- | ------------------------------------------------------------------------- |
| Bryan   | Constraint Helper Functions      | Created reusable constraint plotting utilities used across the project    |
| Deep    | 2D Simplex Visualization         | Implemented tableau Simplex with step-by-step visualization               |
| Gurjas  | Higher-Dimensional Visualization | Created PCA, parallel coordinates, and correlation heatmap visualizations |
| Japneet | Network LP Solver                | Parsed and solved the long15.mps network LP benchmark                     |
| Jovan   | Library Solver                   | Implemented 5+ constraint LP solver using PuLP                            |
| Nishant | Integration & Testing            | Created main runner script and ensured all components work together       |

---

## Project Structure

```
COMP359-Assignment3/
│
├── README.md
│
├── Bryan/
│   ├── constraints.py          # Constraint helper functions
│   └── test_plot.png           # Test output
│
├── deep/
│   ├── simplex_2d.py           # 2D Simplex algorithm implementation
│   ├── plot_all.py             # Combines step images
│   ├── simplex_2d_step_1.png   # Step 1 visualization
│   ├── simplex_2d_step_2.png   # Step 2 visualization
│   ├── simplex_2d_step_3.png   # Step 3 visualization
│   └── simplex_2d_all.png      # Combined visualization
│
├── Jovan/
│   ├── library_solver.py       # LP solver with 5+ constraints
│   └── solution_plot.png       # Solution visualization
│
├── Japneet/
│   ├── network_lp.py           # Network LP solver (long15.mps)
│   ├── solution_summary.txt    # Solution results
│   └── data/
│       ├── long15.mps.bz2      # Downloaded dataset
│       └── long15.mps          # Extracted MPS file
│
├── Gurjas/
│   ├── higher_dim_viz.py       # High-dimensional visualizations
│   ├── pca_visualization.png   # PCA reduction plot
│   ├── parallel_coordinates.png # Parallel coordinates plot
│   ├── correlation_heatmap.png # Correlation heatmap
│   └── network_variable_distribution.png # Variable distribution
│
└── Nishant/
    ├── requirements.txt        # Python dependencies
    └── run_all.py             # Main integration script
```

---

## Setup Instructions

### Prerequisites

* Python 3.8 or higher
* pip3 package manager

### Step 1: Install Dependencies

```bash
pip3 install -r Nishant/requirements.txt
```

Required packages:

* `pulp` - Linear programming solver
* `numpy` - Numerical computations
* `matplotlib` - Visualization
* `scikit-learn` - PCA for dimensionality reduction
* `scipy` - Scientific computing

### Step 2: Run the Complete Project

```bash
python3 Nishant/run_all.py
```

### Step 3: Run Individual Components

```bash
# Bryan's constraint helpers
python3 Bryan/constraints.py

# Deep's 2D simplex visualization
python3 deep/simplex_2d.py
python3 deep/plot_all.py

# Jovan's library solver
python3 Jovan/library_solver.py

# Japneet's network LP
python3 Japneet/network_lp.py

# Gurjas's high-dimensional visualization
python3 Gurjas/higher_dim_viz.py
```

---

## Output Files

### Bryan

| File                  | Description                                     |
| --------------------- | ----------------------------------------------- |
| `Bryan/test_plot.png` | Test plot verifying constraint helper functions |

### Deep

| File                         | Description                      |
| ---------------------------- | -------------------------------- |
| `deep/simplex_2d_step_1.png` | Initial BFS at origin (0,0)      |
| `deep/simplex_2d_step_2.png` | After first pivot (4,0)          |
| `deep/simplex_2d_step_3.png` | Optimal vertex (2,4)             |
| `deep/simplex_2d_all.png`    | Combined view of all three steps |

### Jovan

| File                      | Description                                                   |
| ------------------------- | ------------------------------------------------------------- |
| `Jovan/solution_plot.png` | Feasible region and optimal solution for 7-constraint problem |

### Japneet

| File                           | Description                                                                    |
| ------------------------------ | ------------------------------------------------------------------------------ |
| `Japneet/solution_summary.txt` | Status, objective value, solve time, variable/constraint counts for long15.mps |

### Gurjas

| File                                       | Description                                        |
| ------------------------------------------ | -------------------------------------------------- |
| `Gurjas/pca_visualization.png`             | 50D data reduced to 2D using PCA                   |
| `Gurjas/parallel_coordinates.png`          | Parallel coordinates plot of high-dimensional data |
| `Gurjas/correlation_heatmap.png`           | Correlation matrix of dimensions                   |
| `Gurjas/network_variable_distribution.png` | Distribution of variable values                    |

---

### Japneet's Network LP

* **Dataset**: long15.mps from Mittelmann Network-LP Benchmark
* **Source**: [https://plato.asu.edu/ftp/lptestset/network/](https://plato.asu.edu/ftp/lptestset/network/)
* **Type**: Large-scale network flow problem

---

## Visualization Techniques

### 2D Simplex (Deep)

* Feasible region polygon
* Constraint boundary lines
* Step-by-step corner point progression
* Objective function lines at each iteration

### High-Dimensional (Gurjas)

* **PCA**: Reduces 50 dimensions to 2D while preserving variance
* **Parallel Coordinates**: Shows relationships across multiple dimensions
* **Correlation Heatmap**: Visualizes dimension correlations
* **Distribution Plot**: Shows value distribution across variables

---

## References

### Tools & Libraries

* PuLP Documentation: [https://coin-or.github.io/pulp/](https://coin-or.github.io/pulp/)
* NumPy - Numerical Computing ([https://numpy.org/](https://numpy.org/))
* Matplotlib - Plotting Library ([https://matplotlib.org/](https://matplotlib.org/))
* scikit-learn - Machine Learning Library ([https://scikit-learn.org/](https://scikit-learn.org/))

### Datasets

* Mittelmann Benchmarks: [https://mattmilten.github.io/mittelmann-plots/](https://mattmilten.github.io/mittelmann-plots/)
* Network LP Dataset: [https://plato.asu.edu/ftp/lptestset/network/](https://plato.asu.edu/ftp/lptestset/network/)

### Resources

* Cornell University Computational Optimization Open Textbook: [https://optimization.cbe.cornell.edu/index.php?title=Main_Page]

### AI Usage Disclosure

This project used AI-assisted coding for:

* Generating starter code structure
* Debugging visualization functions
* Code formatting and documentation
* Adding comments to code and making the code efficient


All AI-generated code was reviewed, tested, and integrated by team members.

---


## Submission Notes

The project is submitted as a git bundle. To recreate:

```bash
git bundle create comp359-assignment3.bundle main
```

---
