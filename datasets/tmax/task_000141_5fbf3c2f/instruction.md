You are a Machine Learning Engineer preparing synthetic training data for a spatial regression model. You need to generate correlated multivariate normal samples based on a known covariance structure.

Your task is to write a C program that uses Monte Carlo simulation and Matrix Decomposition to generate these samples, and saves them in a standard scientific format.

The target covariance matrix is stored in `/home/user/cov_matrix.txt`. It is a 4x4 symmetric positive-definite matrix, with space-separated values.

Write and execute a C program (e.g., at `/home/user/gen_samples.c`) that does the following:
1. Reads the 4x4 covariance matrix from `/home/user/cov_matrix.txt`.
2. Computes the Cholesky decomposition of this matrix ($L$, such that $LL^T = \text{Covariance}$).
3. Generates 500,000 independent samples of a 4-dimensional multivariate normal distribution with a mean of 0 and the provided covariance matrix. You should use a standard method (like Box-Muller) to generate standard normal variables, and multiply by the Cholesky factor to induce the correlation.
4. Writes the generated samples (a 500,000 x 4 array of double-precision floats) to an HDF5 file located at `/home/user/synthetic_data.h5`.
5. The data inside the HDF5 file must be stored in a single dataset named `samples`.

Environment notes:
- The standard math library (`libm`) and HDF5 C development headers/libraries (`libhdf5-dev`) are available on the system. Compile your program linking against these libraries (e.g., `-lhdf5 -lm`).
- You can use any standard C libraries (C99 or later).
- Do not use external libraries for the Cholesky decomposition; implement a simple 4x4 Cholesky decomposition directly in your C code.