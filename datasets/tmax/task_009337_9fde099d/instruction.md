As a machine learning engineer, I'm preparing a training dataset of covariance matrices. We've noticed that some of our generated matrices are near-singular or not positive definite, which causes numerical instability during downstream processing. I need you to write a Go program to filter these matrices and report on their numerical stability.

Please perform the following steps:
1. Set up a new Go module named `matrixprep` in the directory `/home/user/matrix_prep`.
2. Use the `gonum.org/v1/gonum/mat` package to handle matrix operations.
3. You will find 10 symmetric 3x3 matrices in the directory `/home/user/data`, named `matrix_0.csv` to `matrix_9.csv`. Each file has no headers and contains 3 rows of 3 comma-separated floats.
4. Write a Go program (e.g., `main.go`) that iterates through all 10 matrices (from 0 to 9). For each matrix $A$:
   - Load the data into a Gonum symmetric dense matrix (`mat.NewSymDense`).
   - Attempt to compute the Cholesky factorization ($A = L L^T$).
   - If the factorization fails (e.g., the matrix is not positive definite), mark it as `failed` and record the error as `-1.000000e+00`.
   - If the factorization succeeds, compute the reconstructed matrix $A' = L L^T$.
   - Calculate the reconstruction error as the **maximum absolute difference** between any corresponding elements of $A$ and $A'$.
   - If the reconstruction error is greater than `1e-8`, mark the matrix as `unstable`.
   - Otherwise, mark it as `stable`.
5. Run your program and ensure it writes the results to `/home/user/matrix_prep/report.csv`. 
   - The CSV must have the exact header: `matrix_id,status,error`
   - `matrix_id` is the integer ID of the matrix (0 to 9).
   - `status` is one of `stable`, `unstable`, or `failed`.
   - `error` is the calculated maximum absolute difference, formatted in scientific notation with 6 decimal places (e.g., `1.234567e-16`), or `-1.000000e+00` for failed factorizations.

Ensure that the output file `/home/user/matrix_prep/report.csv` is correctly created with all 10 rows (plus the header).