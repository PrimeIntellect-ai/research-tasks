You are a data scientist working on a linear model $X\beta = y$, but the design matrix $X$ is highly collinear (near-singular). Standard factorization methods like LU or Cholesky fail or produce wildly unstable coefficients.

You have been provided with an HDF5 file located at `/home/user/data.h5` containing two datasets:
- `X`: A matrix of shape (500, 30)
- `y`: A target vector of shape (500,)

Your task is to write and execute a Python script (`/home/user/solve.py`) to robustly solve this system using the Truncated Singular Value Decomposition (SVD) and perform a subsequent nonlinear equation solving step.

Requirements:
1. Read `X` and `y` from `/home/user/data.h5`.
2. Compute the SVD of $X$.
3. Compute the effective rank of $X$ by counting the number of singular values strictly greater than `1e-8`.
4. Construct the truncated pseudo-inverse of $X$ by setting the reciprocals of singular values $\le 1e-8$ to exactly 0.
5. Compute the robust coefficient vector $\beta = X_{trunc}^+ y$.
6. Calculate the L2 norm of the residuals: $E = ||X\beta - y||_2$.
7. Extract the first three coefficients of $\beta$ (i.e., $\beta_0, \beta_1, \beta_2$) and treat them as the coefficients of a quadratic equation: $f(z) = \beta_0 z^2 + \beta_1 z + \beta_2 = 0$. Find the roots of this polynomial and identify the maximum real part among the roots, let's call it $R$.
8. Save your results to a JSON file at `/home/user/solution.json` with exactly the following structure:
```json
{
  "effective_rank": <int>,
  "residual_norm": <float>,
  "largest_root_real_part": <float>
}
```

Ensure your Python script creates the output file successfully.