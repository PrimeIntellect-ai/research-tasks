You are a machine learning engineer preparing synthetic training data for a spectroscopy model. You plan to use the Cholesky decomposition of the dataset's covariance matrix to generate new samples. However, you've noticed that your data matrix is near-singular, which causes the standard Cholesky decomposition to fail or become numerically unstable.

To fix this, you will apply Tikhonov regularization by adding $\lambda I$ to the covariance matrix $C$. You need to choose between two hypotheses for the regularization parameter: $\lambda_1 = 0.01$ and $\lambda_2 = 0.5$.

Write a C program that performs the following steps:
1. Reads the spectroscopy data from `/home/user/spectra.csv`. The file contains 50 rows (samples) and 10 columns (features), separated by commas.
2. Computes the $10 \times 10$ unbiased sample covariance matrix $C$ of the features.
3. Computes the condition number (the ratio of the largest singular value to the smallest singular value) of the regularized matrix $C_1 = C + 0.01 I$.
4. If the condition number of $C_1$ is strictly greater than 500, reject the $\lambda_1$ hypothesis and select $\lambda_2 = 0.5$. Otherwise, keep $\lambda_1 = 0.01$.
5. Let $\lambda$ be your selected parameter. Compute the Cholesky decomposition of the matrix $C + \lambda I = L L^T$, where $L$ is a lower triangular matrix.
6. Calculate the trace of $L$ (the sum of its diagonal elements).
7. Write the selected $\lambda$ and the trace of $L$ to a file named `/home/user/result.txt` exactly in this format:
   `Lambda: [value], Trace: [value]`
   where both values are formatted to 4 decimal places (e.g., `Lambda: 0.5000, Trace: 8.1234`).

Constraints and details:
- You must use **C** for the implementation.
- You may use the GNU Scientific Library (GSL) for matrix operations (SVD, Cholesky, etc.). Make sure to link against it properly (`-lgsl -lgslcblas -lm`).
- Assume `libgsl-dev` is already installed on the system (if not, you can install it using the standard package manager).
- The unbiased sample covariance between feature $j$ and feature $k$ is calculated as $\frac{1}{N-1} \sum_{i=1}^N (X_{i,j} - \bar{X}_j)(X_{i,k} - \bar{X}_k)$.