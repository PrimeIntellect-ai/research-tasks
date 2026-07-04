I am a researcher running simulations that generate large numbers of covariance matrices. I've been running into reproducibility issues because of floating-point reduction order and precision loss when aggregating my results across different runs. 

Please write a Python script at `/home/user/analyze_covariances.py` that performs the following pipeline exactly, ensuring strict deterministic floating-point operations.

1. **Setup**: Use `numpy` and `scipy`. Set the random seed via `numpy.random.seed(42)`.
2. **Data Generation**: 
   - Generate a 3D multi-dimensional array `A` of shape `(2500, 5, 5)` using standard normal random variables (`np.random.randn`).
   - Construct a set of 2500 symmetric positive-definite matrices `M` by computing $M_i = A_i A_i^T + 0.01 I$, where $I$ is the 5x5 identity matrix. Do this using vectorized multi-dimensional array manipulation.
3. **Matrix Decomposition**:
   - Compute the lower Cholesky decomposition $L_i$ for each matrix $M_i$.
   - For each Cholesky factor $L_i$, compute its singular values using SVD. Extract the largest singular value $s_i$ for each matrix.
4. **Stable Aggregation**:
   - To avoid our previous floating-point reduction order issues, sort the 2500 largest singular values ($s$) in strictly ascending order.
   - Compute the exact sum of these sorted values using Python's `math.fsum()`. Divide by 2500 to get the `stable_mean`.
5. **Density Estimation**:
   - Fit a Gaussian Kernel Density Estimator (using `scipy.stats.gaussian_kde`) to the unsorted array of largest singular values $s$. Use the default bandwidth estimator.
   - Evaluate the estimated probability density function at the point $x = 6.0$, let's call this `kde_val`.

Your script should execute this pipeline and write exactly two lines to `/home/user/results.txt` in the following format (round both values to exactly 6 decimal places):
```
Stable Mean: <stable_mean>
KDE at 6.0: <kde_val>
```

Execute your script to produce the output file.