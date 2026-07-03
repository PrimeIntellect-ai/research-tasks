You are a performance engineer analyzing a molecular dynamics profiling application. The existing codebase reads spatial coordinates from a Protein Data Bank (PDB) file to compute the spatial covariance matrix of the atoms. However, the application crashes on a specific PDB file because the atoms are coplanar, resulting in a singular covariance matrix that cannot be inverted.

Your task is to fix the application by implementing Tikhonov regularization, then use numerical integration and statistical hypothesis testing to profile the matrix's stability.

Here is the step-by-step specification:

1. **Parse the PDB Data**: 
   Write a Go program in `/home/user/profiler/main.go` (you will need to initialize a Go module and write it from scratch or modify existing files). The program must read the file at `/home/user/data/input.pdb`. Extract the X, Y, and Z coordinates for all atoms (ignore atom type, just read the coordinates from standard PDB columns: X is columns 31-38, Y is 39-46, Z is 47-54).

2. **Compute the Regularized Covariance Matrix**:
   Compute the 3x3 unbiased sample covariance matrix $C$ of the (X, Y, Z) coordinates. 
   To solve the singularity issue, apply Tikhonov regularization by adding a penalty parameter $\lambda$ to the diagonal elements: $C_{reg}(\lambda) = C + \lambda I$, where $I$ is the 3x3 identity matrix.

3. **Numerical Integration (Stability Profiling)**:
   We need to profile the trace of the inverse of this regularized matrix: $f(\lambda) = \text{Trace}(C_{reg}(\lambda)^{-1})$.
   Implement a numerical integration function using the **Trapezoidal rule** to integrate $f(\lambda)$ from $\lambda = 0.1$ to $\lambda = 1.0$, using exactly $N = 1000$ intervals (i.e., 1001 evaluation points including the endpoints). 
   *Note: You may use a third-party linear algebra library like `gonum.org/v1/gonum/mat` to perform the matrix inversion, or write your own 3x3 analytical inversion.*

4. **Statistical Hypothesis Testing**:
   Perform a one-sample t-test on the extracted X coordinates to test the null hypothesis that the population mean of X is zero ($\mu_X = 0$). Calculate the t-statistic: $t = \frac{\bar{X} - 0}{s_X / \sqrt{n}}$, where $\bar{X}$ is the sample mean, $s_X$ is the sample standard deviation, and $n$ is the number of atoms.

5. **Output**:
   Your Go program must create a file at `/home/user/output.txt` containing exactly two lines with the computed values formatted to 4 decimal places:
   ```
   Integral: [computed_integral]
   t-stat: [computed_t_statistic]
   ```

Complete the implementation, build, and run your Go program to produce the target output file.