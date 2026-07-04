You are a data engineer building a high-performance C-based ETL pipeline. Part of this pipeline involves a dimensionality reduction step where high-dimensional sensor data (10D) is projected into a lower-dimensional space (3D) using a pre-computed projection matrix.

Your task is to write a C program that validates this projection step using a fast numerical linear algebra library.

Specifically, you need to:
1. Install the OpenBLAS library and its C headers on the system.
2. Write a C program at `/home/user/validate_pca.c` that does the following:
   - Reads three space-separated text files containing double-precision floating-point numbers:
     - `/home/user/X.txt`: The input data matrix (100 rows, 10 columns).
     - `/home/user/P.txt`: The projection matrix (10 rows, 3 columns).
     - `/home/user/Y_ref.txt`: The reference output data matrix (100 rows, 3 columns).
   - Uses `cblas_dgemm` from the OpenBLAS library to compute the matrix multiplication $Y = X \times P$. 
   - Note: In C, 2D arrays read sequentially from text files are usually in row-major order (CblasRowMajor).
   - Computes the maximum absolute difference (error) between the computed matrix $Y$ and the reference matrix `Y_ref`.
   - Writes only this maximum absolute difference as a float with 6 decimal places (e.g., `0.000015`) to `/home/user/max_diff.txt`.
3. Compile your program to `/home/user/validate_pca` and run it to produce the `max_diff.txt` file.

Assume all files contain properly formatted space-separated values without headers. Do not hardcode the expected error; you must compute it.