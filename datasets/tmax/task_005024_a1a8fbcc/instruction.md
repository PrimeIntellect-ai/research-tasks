You are tasked with deploying and using a custom Bayesian inference pipeline for a data science project. The workflow involves fixing a broken local Python extension, and then writing a script that uses it alongside matrix decompositions and Monte Carlo / Bootstrap techniques to process feature vectors and output prediction intervals.

**Part 1: Fix and Install the Vendored Package**
We have a proprietary Python package located at `/app/poly_basis/`. This package contains a fast Cython implementation for polynomial feature expansion. 
Currently, the package fails to install because of a configuration error in its build setup (specifically, the `setup.py` is incorrectly configured to compile a `.c` file that doesn't exist, rather than using Cython to compile the `.pyx` file). 
1. Fix the `setup.py` in `/app/poly_basis/` so it correctly uses `Cython.Build.cythonize` on `poly_basis.pyx`.
2. Install the package into your Python environment.

**Part 2: Implement the Prediction Script**
Write a Python script at `/home/user/run_model.py`. This script will be executed with a variable number of floating-point arguments representing a feature vector `x`.
Example invocation: `python /home/user/run_model.py 1.5 -2.3 0.4`

The script must perform the exact following deterministic steps:
1. Parse the command-line arguments into a 1D NumPy float64 array `x`.
2. Use the fixed `poly_basis` package to expand `x`: `from poly_basis import expand; x_poly = expand(x, degree=3)`. 
3. Load the pre-computed MCMC posterior samples of the weights from `/app/data/posterior_weights.npy` (this is a 2D array of shape `(n_samples, n_features)`).
4. Load the covariance scaling matrix `S` from `/app/data/scale_matrix.npy`.
5. **Matrix Decomposition:** Compute the lower Cholesky factor $L$ of `S`. 
6. Adjust the feature vector by solving the linear system $L z = x\_poly$ (you can use `scipy.linalg.solve_triangular`).
7. **Posterior Estimation:** Multiply the adjusted feature vector $z$ by the posterior weights to get a 1D array of posterior predictions `y_preds = posterior_weights @ z`.
8. **Bootstrap Confidence Intervals:** We want the 95% confidence interval of the *median* of the predictions.
   - Initialize a NumPy random generator exactly as: `rng = np.random.default_rng(seed=int(np.sum(np.abs(x)) * 1000))`
   - Perform exactly 2000 Bootstrap resamples (with replacement) of the `y_preds` array.
   - For each resample, calculate the median.
   - Calculate the 2.5th and 97.5th percentiles of these 2000 medians using `numpy.percentile` with the default settings.
9. **Output:** The script must print exactly one line to standard output in the following format:
`Mean: <mean_of_y_preds>, CI: [<lower_bound>, <upper_bound>]`
Format the three numbers to exactly 4 decimal places.

Your script must produce *bit-exact* output identical to our reference implementation for any given input vector. Do not add any extra print statements.