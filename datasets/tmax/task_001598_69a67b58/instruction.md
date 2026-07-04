You are an AI assistant acting as a data scientist. We have a dynamical system that occasionally diverges. You need to analyze the trajectories, model the nominal behavior, and identify which trajectories have diverged by comparing them against a reference dataset of stable behavior.

Your tasks are:
1. **Data Preprocessing & Dimensionality Reduction**:
   - Load `/home/user/trajectories.csv`. This file contains the columns `id`, `time`, `x1`, `x2`, `x3`, `x4`, and `x5`.
   - Extract the features `x1` through `x5` as a matrix $X$.
   - Center the data by subtracting the mean of each column.
   - Perform Singular Value Decomposition (SVD) on the centered data matrix to find the principal components.
   - Project the centered data onto the first two principal components (those corresponding to the two largest singular values) to get the 2D coordinates $Z_1$ and $Z_2$.
   - *Sign ambiguity resolution*: Let $v_1$ and $v_2$ be the first two principal component vectors (the right singular vectors, each of length 5). If the sum of the elements of $v_1$ is negative, multiply $v_1$ and $Z_1$ by -1. Do the same for $v_2$ and $Z_2$.

2. **Curve Fitting**:
   - Model the nominal trajectory path in the 2D projected space by fitting a cubic polynomial regression: $Z_2 = a Z_1^3 + b Z_1^2 + c Z_1 + d$.
   - Use standard ordinary least squares for this fit.

3. **Residual Calculation**:
   - For every point in the dataset, calculate the absolute residual from the fitted curve: $r = |Z_2 - (a Z_1^3 + b Z_1^2 + c Z_1 + d)|$.
   - For each trajectory (grouped by `id`), calculate its maximum residual: $R_{id} = \max_{i \in \text{traj}} r_i$.

4. **Reference Dataset Comparison & Density Estimation**:
   - Load `/home/user/reference_residuals.csv`, which contains a single column `residual` representing the maximum residuals of known stable trajectories.
   - Fit a Gaussian Kernel Density Estimate (KDE) to this reference data using `scipy.stats.gaussian_kde` with `bw_method=0.2`.
   - Calculate the 95th percentile threshold $T$ of this KDE distribution. Specifically, find $T$ such that the integral of the KDE PDF from $-\infty$ to $T$ is exactly `0.95`. (You can use `scipy.optimize` and `kde.integrate_box_1d` or similar methods).

5. **Classification**:
   - Identify all trajectory IDs where $R_{id} > T$. These are the divergent trajectories.

6. **Output**:
   - Save your final results in a JSON file at `/home/user/results.json` with the following structure:
     ```json
     {
       "polynomial_coefficients": [a, b, c, d],
       "threshold": 1.234567,
       "divergent_trajectory_ids": [1, 5, 8, ...]
     }
     ```
   - Make sure `polynomial_coefficients` contains exactly 4 floats in the order $[a, b, c, d]$.
   - Sort the `divergent_trajectory_ids` in ascending order.