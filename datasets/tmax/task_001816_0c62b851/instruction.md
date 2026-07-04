You are acting as a Machine Learning Engineer preparing spatial training data for a neural network. You need to normalize the features based on localized density structures in the data.

You have been provided with a dataset of 2D coordinates in `/home/user/points.csv`. The file has no header and contains `x,y` pairs on each line. 

Your task is to write a script (in any language you choose, though Python with `scipy` and `numpy` is highly recommended for reproducibility) that performs the following steps:

1. **Density Estimation:** Fit a Gaussian Kernel Density Estimator (KDE) to the points. Evaluate this KDE on a $100 \times 100$ uniform mesh grid over the domain $x \in [-10, 10]$ and $y \in [-10, 10]$. (Generate the grid using 100 linearly spaced points from -10 to 10 inclusive for both $x$ and $y$). Note: If using Python, use `scipy.stats.gaussian_kde` with its default bandwidth (Scott's Rule).
2. **Domain Decomposition:** Identify the specific point $(x^*, y^*)$ on your $100 \times 100$ mesh grid where the KDE density is maximized. Use this point as the origin to decompose the domain into 4 quadrants (Top-Right, Top-Left, Bottom-Left, Bottom-Right). Assign each point from the original `points.csv` dataset into one of these 4 sub-domains based on its relation to $(x^*, y^*)$.
3. **Matrix Decomposition:** For the subset of original data points falling into *each* of the 4 sub-domains, compute the $2 \times 2$ sample covariance matrix $\Sigma$. Then, compute the Cholesky decomposition $L$ for each covariance matrix (where $\Sigma = L L^T$ and $L$ is a lower triangular matrix). 
   *Note: If a sub-domain has fewer than 2 points, treat its covariance matrix as a matrix of zeros and the resulting $L$ trace as 0.*
4. **Extraction:** Calculate the trace (sum of the main diagonal elements) of the Cholesky factor $L$ for each of the 4 sub-domains.
5. **Output:** Save the 4 trace values to a file named `/home/user/traces.txt`. The file must contain one value per line, sorted in **ascending numeric order**, and formatted to exactly 4 decimal places (e.g., `1.2345`).

Deliver the exact file `/home/user/traces.txt` as described. You may run any commands in the terminal to accomplish this.