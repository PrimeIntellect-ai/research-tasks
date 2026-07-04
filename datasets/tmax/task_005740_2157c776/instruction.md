You are an assistant helping a computational biology researcher. The researcher is attempting to predict protein stability traits ($y$) based on three extracted structural features ($x_1, x_2, x_3$).

The researcher tried using standard ordinary least squares (OLS) regression to find the optimal feature weights $w$ by solving the normal equations $A w = b$, where $A = X^T X$ and $b = X^T y$. However, the extracted features are highly collinear (near-singular input matrix), causing their C++ matrix factorization to fail or produce NaNs. 

Your task is to write a complete C++ program that implements Tikhonov regularization (Ridge Regression) to stabilize the matrix inversion.

1. **Input Data**: The observational data is located at `/home/user/protein_features.csv`.
   Each line contains four comma-separated floating-point numbers: `x1, x2, x3, y`.
   
2. **Algorithm Requirements**:
   - Parse the CSV to construct the $N \times 3$ design matrix $X$ and the $N \times 1$ vector $y$.
   - Compute the covariance matrix $A = X^T X$ and the vector $b = X^T y$.
   - Apply Tikhonov regularization by adding a penalty term to the diagonal of $A$: $A_{reg} = A + \lambda I$, where $\lambda = 0.05$ and $I$ is the $3 \times 3$ identity matrix.
   - Solve the stabilized linear system $A_{reg} w = b$ for the weight vector $w$.
   
3. **Implementation**:
   - Write your C++ code to a file named `/home/user/solve_weights.cpp`.
   - You may write your own simple $3 \times 3$ matrix solver (e.g., Cramer's rule or Gaussian elimination) or use standard C++ libraries. Do not rely on external libraries like Eigen being pre-installed unless you fetch them locally without root.
   - Compile and run your program.

4. **Output Format**:
   - The program must write the final three weights ($w_1, w_2, w_3$) to `/home/user/weights.csv`.
   - The output file must contain exactly one line with the three floating-point values separated by commas (e.g., `1.234,5.678,-0.910`).

Please execute the necessary commands to create the input file (as a placeholder if it doesn't exist, but assume it will be placed there by the system), write the C++ program, compile it, and generate the required output.