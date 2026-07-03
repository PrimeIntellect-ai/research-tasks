You are assisting a researcher who is running sensor network simulations. The simulation produces a $5 \times 5$ spatial covariance matrix representing sensor noise. However, because two sensors are placed very close to each other, the matrix is near-singular (ill-conditioned) and strictly not positive-definite due to numerical precision issues.

Your task is to write a C program that applies Tikhonov regularization to make the matrix positive-definite, performs a Cholesky decomposition ($A_{reg} = L L^T$), and validates the decomposition.

Here are the specific steps:
1. **Input Data**: The covariance matrix is located at `/home/user/cov_matrix.csv`. It is a 5x5 matrix of comma-separated floating-point numbers.
2. **Regularization**: Write a C program (`/home/user/process_cov.c`) that reads this CSV file. Add a regularization term $\lambda = 1 \times 10^{-4}$ to the main diagonal of the matrix. Let this new matrix be $A_{reg} = A + \lambda I$.
3. **Decomposition**: Implement a standard Cholesky decomposition algorithm from scratch in C to decompose $A_{reg}$ into a lower triangular matrix $L$.
4. **Validation**: Compute the reconstructed matrix $A_{recon} = L L^T$. Calculate the Frobenius norm of the difference between the reconstructed matrix and the regularized matrix: $E = ||A_{recon} - A_{reg}||_F$. 
5. **Output**: Your C program must write the results to `/home/user/decomposition_results.log` in the exact following format:

```text
Error_Frobenius: [Value in scientific notation, e.g., 1.23e-15]
L_Matrix:
[L_00], 0.000000, 0.000000, 0.000000, 0.000000
[L_10], [L_11], 0.000000, 0.000000, 0.000000
[L_20], [L_21], [L_22], 0.000000, 0.000000
[L_30], [L_31], [L_32], [L_33], 0.000000
[L_40], [L_41], [L_42], [L_43], [L_44]
```
Format the matrix elements to exactly 6 decimal places (e.g., `%.6f`).

You must compile your program using standard GCC tools (e.g., `gcc -o process_cov process_cov.c -lm`) and run it to produce the log file. You do not need to use external libraries like LAPACK or BLAS; implement the standard Cholesky algorithm directly in your C code.