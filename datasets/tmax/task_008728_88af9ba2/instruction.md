You are acting as a machine learning engineer preparing a dataset for a generative model. 

I have a set of 3x3 covariance matrices stored in an HDF5 file at `/home/user/covariances.h5` under the dataset name `cov_matrices` (shape: `N x 3 x 3`). I am trying to compute the Cholesky decomposition of these matrices to generate whitening transformations. However, my pipeline keeps failing because some of these matrices are near-singular or not strictly positive-definite due to floating-point errors from previous processing steps.

Your task is to write a C++ program at `/home/user/process_covs.cpp` that reads this HDF5 file and robustly computes the Cholesky factor $L$ (where $\Sigma = L L^T$ and $L$ is lower-triangular) for each matrix. 

If a matrix fails the Cholesky decomposition, apply Tikhonov regularization by adding $\lambda I$ to the matrix (where $I$ is the 3x3 identity matrix and $\lambda$ starts at $10^{-4}$). If it still fails, increment $\lambda$ by $10^{-4}$ and retry until the decomposition succeeds. 

For each matrix in the dataset (index $0$ to $N-1$), compute:
1. The final $\lambda$ added to make it positive definite ($\lambda=0$ if it succeeded originally).
2. The trace of the resulting lower-triangular Cholesky factor $L$.

Write the results to a CSV file at `/home/user/results.csv` with the following format exactly (including the header):
```csv
index,lambda,trace_L
0,0.0000,3.1415
1,0.0001,2.7182
...
```
Output the floating-point values to 4 decimal places.

You can use the `libhdf5-dev` library and the `Eigen3` library (which provides `Eigen::LLT` for Cholesky decomposition). You may need to install them or relevant C++ HDF5 wrappers (like HighFive, or just use the C API) depending on your approach. Compile your program to `/home/user/process_covs` and run it to produce the `results.csv` file.