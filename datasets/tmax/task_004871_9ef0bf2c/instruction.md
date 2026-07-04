You are a data scientist fitting a spatial regression model. Your team has developed a prototype script located at `/home/user/fit_model.py` that discretizes a 1D spatial domain $x \in [0, 1]$ into $N$ nodes, assembles a stiffness matrix $A$ (a simple 1D Laplacian) and a load vector $b$ from a dataset of point measurements, and solves the linear system $Ax = b$ to find the spatial field $x$.

However, there are several issues with the current implementation that you must resolve:

1. **Non-reproducibility**: The results vary slightly across different runs. The current script reads data points and aggregates their values into the load vector $b$. Due to how the aggregation is implemented using unordered collections, floating-point reduction order causes non-deterministic variations in the assembled vector $b$, leading to unstable model fits. You must find and fix this non-deterministic aggregation in the code so that the assembled $b$ (and thus the solution) is exactly identical across multiple runs. Accumulate the weights in the exact order they appear in the original input data.
2. **Matrix Decomposition**: The script currently uses a generic solver. Update the script to specifically use Cholesky decomposition (`scipy.linalg.cho_factor` and `scipy.linalg.cho_solve`) to solve the system, as $A$ is symmetric positive-definite.
3. **Mesh Refinement & Stability**: Implement a mesh refinement study to test numerical stability. Instead of solving for a single hardcoded $N$, your script must solve the system for a coarse mesh ($N=10$) and a fine mesh ($N=20$).
4. **Analysis Output**: For both $N=10$ and $N=20$, calculate the condition number of the matrix $A$ (using `numpy.linalg.cond` with the default 2-norm) and the L2 norm of the solution vector $x$ (using `numpy.linalg.norm`).

Write your final computed metrics to a JSON file at `/home/user/stability_report.json`. The file must exactly match this structure:
```json
{
  "N_10": {
    "cond_A": <float>,
    "norm_x": <float>
  },
  "N_20": {
    "cond_A": <float>,
    "norm_x": <float>
  }
}
```

The dataset is located at `/home/user/data.csv`. Do not modify the dataset file. Ensure your modified `fit_model.py` script runs cleanly without errors.