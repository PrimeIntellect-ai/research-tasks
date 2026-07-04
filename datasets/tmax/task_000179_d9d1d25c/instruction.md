You are a data scientist tasked with debugging a brittle modeling pipeline and replacing it with a robust, numerically stable alternative. 

You have been given a dataset `/home/user/X.csv` (features) and `/home/user/y.csv` (targets), and the source code for a custom C-extension `/home/user/src/naive_solver.c` that performs ordinary least squares (OLS) via naive Gaussian elimination without pivoting.

Your task is to orchestrate a workflow that demonstrates the numerical instability of the naive C implementation on near-singular data, and then implements a stable fallback with statistical confidence bounds.

Follow these steps exactly:

1. **Compile the Custom Software:**
   Compile `/home/user/src/naive_solver.c` into a shared library named `/home/user/src/libnaive.so`. 

2. **Numerical Stability Testing:**
   Write a Python script `/home/user/workflow.py` that:
   - Loads `X.csv` and `y.csv`.
   - Forms the normal equations: $A = X^T X$ and $b = X^T y$.
   - Uses `ctypes` to call the `solve_system(double* A, double* b, int n, double* x)` function from `libnaive.so` to solve for coefficients $\beta$. (Note: $A$ is an $n \times n$ matrix flattened in row-major order, $b$ is length $n$, and $x$ is an output array of length $n$).
   - Calculates the L2 norm of the residuals ($||y - X\beta||_2$) for the naive solver.

3. **Stable Fallback & Bootstrap Confidence Intervals:**
   - The data is highly collinear (near-singular). Implement Ridge Regression in Python using `sklearn.linear_model.Ridge` with `alpha=0.1` (do not fit an intercept, i.e., `fit_intercept=False`).
   - Fit this Ridge model on the full dataset and compute its Mean Squared Error (MSE).
   - Compute a 95% bootstrap confidence interval for this MSE. 
     - Set the random seed: `numpy.random.seed(42)`
     - Perform $B=1000$ bootstrap iterations.
     - In each iteration, sample $N$ (where $N$ is the number of rows in $X$) indices with replacement from $0$ to $N-1$.
     - Extract the resampled $X_{boot}$ and $y_{boot}$.
     - Fit the Ridge model (`alpha=0.1`, `fit_intercept=False`) on the resampled data.
     - Calculate the MSE of the fitted model *on that same resampled data*.
     - Compute the 2.5th and 97.5th percentiles of the 1000 MSE values using `numpy.percentile`.

4. **Results Logging:**
   Your script must output a JSON file at `/home/user/results.json` with exactly these keys:
   - `"unstable_residual_norm"`: Float. The L2 norm of the residuals from the naive C solver.
   - `"stable_ridge_mse"`: Float. The MSE of the Ridge model trained on the full original dataset.
   - `"mse_ci_lower"`: Float. The 2.5th percentile of the bootstrap MSEs.
   - `"mse_ci_upper"`: Float. The 97.5th percentile of the bootstrap MSEs.

Ensure you create and run the Python script to produce the final `results.json` file.