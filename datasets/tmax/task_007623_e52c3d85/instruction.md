You are a data scientist tasked with resolving a reproducible research issue. Our team has been fitting Kernel Density Estimates (KDE) to particle collision datasets. However, we've noticed small numerical discrepancies across different environments when comparing our density maps against a reference dataset, likely due to float32 vs float64 reduction orders. 

We need you to orchestrate an automated, numerically stable Jupyter Notebook workflow.

Here is your task:
1. First, install `papermill`, `jupyter`, `numpy`, `scipy`, `pandas`, and `scikit-learn` if they aren't already installed.
2. Create a Jupyter Notebook at `/home/user/analysis.ipynb`.
3. In this notebook, create a cell tagged with `parameters` containing a single variable: `bandwidth = 0.1`.
4. The notebook must perform the following operations:
   - Load the particle dataset from `/home/user/data/particles.csv`. This file contains `x`, `y`, and `z` columns. You will only use `x` and `y`.
   - Fit a 2D Gaussian KDE using `scipy.stats.gaussian_kde` on the `(x, y)` data. Use the `bandwidth` parameter as the `bw_method`.
   - Load the 2D evaluation grid coordinates from `/home/user/data/grid_X.npy` and `/home/user/data/grid_Y.npy`.
   - Evaluate the KDE on this grid. (Note: `gaussian_kde` expects a 2xN array, so you'll need to flatten the grids, evaluate, and reshape back to the grid's original shape).
   - Load the reference density map from `/home/user/data/reference_density.npy`.
   - To ensure numerical stability, explicitly cast both your evaluated KDE density array and the reference density array to `numpy.float64` *before* calculating their difference.
   - Calculate the Maximum Absolute Difference (MAD) between your evaluated KDE density and the reference density.
   - Write this MAD value (formatted to exactly 6 decimal places, e.g., `0.012345`) to `/home/user/mad_result.txt`.
5. Finally, use the `papermill` command-line tool to execute `/home/user/analysis.ipynb`, injecting the parameter `bandwidth = 0.25`. Save the executed notebook as `/home/user/analysis_out.ipynb`.

The data files in `/home/user/data/` will be available when you begin. Provide the notebook and run it to produce `/home/user/mad_result.txt` and `/home/user/analysis_out.ipynb`.