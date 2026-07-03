You are an AI assistant helping a Machine Learning Engineer prepare spatial training data for a Gaussian Process model. 

You need to write and execute a Python script (`/home/user/prepare_data.py`) that performs a 1D domain decomposition, constructs a covariance matrix, ensures numerical stability, and performs a matrix decomposition.

Here are the precise specifications for the script:
1. **Grid Generation**: Create a 1D uniform grid of 200 points from 0.0 to 1.0 (inclusive) using `numpy.linspace(0, 1, 200)`.
2. **Domain Decomposition**: Split the grid into two equal subdomains: 
   - `Left`: The first 100 points.
   - `Right`: The remaining 100 points.
3. **Covariance Matrix**: For each subdomain, construct a covariance matrix $K$ of shape (100, 100) using the Squared Exponential kernel:
   $K_{i,j} = \exp(-100 \times (x_i - x_j)^2)$
4. **Numerical Stability & Matrix Decomposition**: The theoretical matrix $K$ is positive semi-definite, but numerical errors will make the standard Cholesky decomposition fail. For each subdomain, iteratively attempt a Cholesky decomposition (`numpy.linalg.cholesky`). 
   - Before decomposing, add a diagonal jitter: $K_{stable} = K + j \times I$ where $I$ is the identity matrix.
   - Start with $j = 10^{-8}$. If the Cholesky decomposition raises a `numpy.linalg.LinAlgError`, multiply $j$ by 10 and try again. Repeat until the decomposition succeeds.
   - Let $L$ be the successful lower-triangular Cholesky factor.
5. **Output**: Calculate the trace (sum of the diagonal elements) of $L$ for both the Left and Right subdomains. Write these two values to `/home/user/cholesky_diags.txt`, separated by a comma, formatted to exactly 6 decimal places.
   Example format for the text file: `12.345678,12.345678`

Write the script, run it, and verify that `/home/user/cholesky_diags.txt` is created with the correct format.