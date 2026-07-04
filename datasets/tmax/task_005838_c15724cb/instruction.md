You are acting as a performance engineer optimizing a spectroscopy data processing pipeline. 

In `/home/user/pipeline/`, there is a Python script named `process_spectra.py`. This script reads spectral signal data from `spectra.csv` and target responses from `target.csv`. It attempts to compute a signal projection weight vector $w$ by solving the linear system $C w = y$, where $C$ is the feature covariance matrix of the spectral data, and $y$ is the target vector. 

Currently, the script crashes with a `LinAlgError` because the spectral bands are highly collinear, making the covariance matrix $C$ near-singular. The script wrongly attempts to use a strict Cholesky decomposition (`scipy.linalg.cholesky`), which fails on matrices that aren't strictly positive definite due to numerical limits.

Your task is to fix the pipeline and complete the data processing:

1. Modify `/home/user/pipeline/process_spectra.py`. Remove the failing Cholesky decomposition.
2. Replace it with a robust Singular Value Decomposition (SVD) approach to compute the Moore-Penrose pseudo-inverse of $C$, and use it to solve for $w$ (i.e., $w = C^{+} y$).
3. Compute the projection vector $P = X w$, where $X$ is the original spectral data matrix.
4. Perform density estimation by fitting a Gaussian (Normal) distribution to the projection vector $P$. Calculate the population mean and population standard deviation (using $N$, not $N-1$ for the variance denominator).
5. The script must output these fitted Gaussian parameters to a log file located at `/home/user/pipeline/results.log` in the exact following format (rounded to exactly 4 decimal places):

```text
Mean: <calculated_mean>
StdDev: <calculated_stddev>
```

Make sure your computations use `numpy`'s default `np.std` (which uses `ddof=0`). You can run the script using standard bash commands and Python to verify it executes successfully.