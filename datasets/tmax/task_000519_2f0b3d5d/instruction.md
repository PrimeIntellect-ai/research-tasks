You are a performance engineer profiling a scientific simulation. The simulation produces non-reproducible results across different environments, and you suspect numerical instability in floating-point reductions.

You have been provided with observational data from the simulation in `/home/user/data.npy`. This is a 3D NumPy array of `float32` values.

Your task is to reshape this data, quantify the numerical instability, analyze the principal components of the data, and compute confidence intervals for the error. 

Write a Python script `/home/user/analyze.py` that performs the following steps:

1. **Observational Data Reshaping**: 
   Load `/home/user/data.npy` (shape `(100, 50, 50)`). Reshape it into a 2D matrix of shape `(100, 2500)`, keeping the first axis intact.

2. **Numerical Stability Testing**:
   For each of the 2500 columns in the reshaped matrix, compute the sum of its 100 elements using two methods:
   - *Unstable Sum*: Initialize a counter `s = numpy.float32(0.0)` and add each element of the column sequentially in a loop (`s += val`).
   - *Stable Sum*: Use Python's built-in `math.fsum()` on the column.
   Compute the error for each column as: `error = unstable_sum - stable_sum`.
   Find the maximum absolute error across all 2500 columns.

3. **Matrix Decomposition**:
   Perform Singular Value Decomposition (SVD) on the 2D `(100, 2500)` data matrix using `numpy.linalg.svd` (with `full_matrices=False`). Extract the first right singular vector (the first row of $V^T$). To avoid sign ambiguity, compute the sum of the absolute values of its elements.

4. **Bootstrap Confidence Intervals**:
   Compute a 95% bootstrap confidence interval for the mean of the 2500 `error` values. 
   - Set `numpy.random.seed(42)` immediately before the bootstrap loop.
   - Perform 1000 iterations. In each iteration, sample 2500 error values *with replacement* using `numpy.random.choice`, and compute the mean of the sample.
   - Use `numpy.percentile` to find the 2.5th and 97.5th percentiles of the 1000 sample means.

5. **Output**:
   Save the results to `/home/user/profile_results.json` with exactly these keys:
   - `"max_abs_error"`: The maximum absolute error (float).
   - `"svd_vt0_abs_sum"`: The sum of absolute values of the first right singular vector (float).
   - `"boot_ci_lower"`: The 2.5th percentile of the bootstrap means (float).
   - `"boot_ci_upper"`: The 97.5th percentile of the bootstrap means (float).

Run your script to ensure the JSON file is generated successfully.