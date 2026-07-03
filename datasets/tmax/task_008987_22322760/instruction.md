You are a performance engineer tasked with debugging and fixing a scientific computing application. 

In the directory `/home/user/app/`, there is a C program `poly_fit.c` that performs a polynomial least-squares fit on a dataset using Normal Equations and LU decomposition, and then calculates the integral of the resulting polynomial. The application is meant to compile with `gcc -O2 poly_fit.c -o poly_fit -lm`.

However, the application is failing. The input data provided in `data.csv` (which contains heavily correlated, noisy samples derived from a spectral analysis pipeline) causes the Normal Matrix ($A^T A$) to become near-singular. The custom LU decomposition solver fails (producing NaNs or crashing) because it lacks pivoting and regularization.

Your task is to:
1. Modify `/home/user/app/poly_fit.c` to fix the near-singular matrix issue by implementing Tikhonov regularization (Ridge regression). Specifically, add a regularization parameter $\lambda = 10^{-4}$ to the main diagonal of the $A^T A$ matrix before the LU decomposition step. (i.e., $(A^T A + \lambda I)x = A^T b$).
2. The program currently has a stub function `double integrate_poly(double* coeffs, int degree, double start, double end)` which is supposed to compute the exact analytical definite integral of the resulting polynomial from $x=0$ to $x=10.0$. Implement this function. (The polynomial is of the form $y = c_0 + c_1 x + c_2 x^2 + \dots$, where `coeffs[i]` is $c_i$).
3. Compile the fixed program and run it. 
4. The program must output the final results to `/home/user/app/output.txt` in the following exact format:
```
Coefficients:
c0 = [value]
c1 = [value]
c2 = [value]
c3 = [value]
Integral(0 to 10): [value]
```
Format all floating-point numbers to 4 decimal places (e.g., `%.4f`).

Everything you need to modify is within `/home/user/app/poly_fit.c`. The degree of the polynomial is fixed at 3 (so there are 4 coefficients: $c_0, c_1, c_2, c_3$).