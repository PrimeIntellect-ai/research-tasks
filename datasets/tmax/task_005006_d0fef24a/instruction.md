You are a Machine Learning Engineer preparing synthetic training data. You have been provided with a Go project located in `/home/user/data_prep`.

Inside this directory, there is a `matrix.csv` file containing an empirical covariance matrix, and a `main.go` script. The script currently attempts to read the covariance matrix and perform a Cholesky decomposition using the `gonum.org/v1/gonum/mat` package in order to set up a sampling pipeline. 

However, the empirical covariance matrix is rank-deficient (near-singular) due to highly correlated features in the original dataset. As a result, the Cholesky factorization fails.

Your task is to fix `main.go` by applying a matrix regularization technique. Modify the Go script to perform the following steps:
1. Compute the Singular Value Decomposition (SVD) of the matrix.
2. Inspect the singular values. For any singular value that is strictly less than `0.1`, replace it with exactly `0.1`.
3. Reconstruct the regularized covariance matrix using the modified singular values. (Assume the standard $U \Sigma V^T$ reconstruction).
4. Calculate the trace (sum of the main diagonal elements) of the newly reconstructed regularized covariance matrix.
5. Write this trace value to a file located exactly at `/home/user/trace.txt`, formatted to exactly 4 decimal places (e.g., `12.3456`).

Ensure you run your modified script to generate the output file. You can install any standard Go utilities or modify the `go.mod` file if needed, but the primary logic should be written in Go using the `gonum` library.