You are a performance and numerical stability engineer evaluating mathematical libraries. We need to profile the numerical error convergence of different matrix decomposition-based linear solvers as the problem's condition number degrades.

Your task is to write and execute a script (in the language of your choice, though Python with NumPy/SciPy is highly recommended) that performs this stability profiling. 

Follow these precise steps:
1. Initialize your random number generator with a fixed seed of `42` (e.g., `np.random.seed(42)`).
2. For each target condition number $K \in \{10^2, 10^4, 10^6, 10^8\}$:
   a. Generate a $100 \times 100$ matrix $X$ where each element is drawn from a standard normal distribution $\mathcal{N}(0, 1)$.
   b. Perform a Singular Value Decomposition (SVD) on $X = U \Sigma V^T$.
   c. Create a new set of 100 singular values $\Sigma'$, which are logarithmically spaced from $K$ down to $1$ (inclusive).
   d. Construct the ill-conditioned test matrix $A = U \Sigma' V^T$.
   e. Let $x_{true}$ be a column vector of 100 ones. Compute the right-hand side vector $b = A x_{true}$.
   f. Solve the linear system $A x = b$ to find $x$ using two different methods:
      - **Method 1 (LU):** Standard LU decomposition solver.
      - **Method 2 (QR):** QR decomposition (compute $A = QR$, then solve $R x = Q^T b$).
   g. Calculate the relative $L_2$ error for each method: $E = \frac{||x - x_{true}||_2}{||x_{true}||_2}$.
3. Once you have the relative errors for all $K$, perform a linear regression of $\log_{10}(E)$ against $\log_{10}(K)$ for both the LU and QR methods. Find the slopes (scaling exponents) of these fits, $m_{LU}$ and $m_{QR}$.
4. Save your final computed slopes to `/home/user/stability_report.json` with the following exact schema:
   ```json
   {
     "slope_lu": <float>,
     "slope_qr": <float>
   }
   ```

You will need to install any dependencies you choose to use. Ensure your final output is strictly in the requested JSON format.