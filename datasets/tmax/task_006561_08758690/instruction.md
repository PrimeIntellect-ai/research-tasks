You are acting as a computational assistant for a researcher modeling molecular networks. 

The researcher was trying to compute the log-determinant of a network's Laplacian matrix using Cholesky decomposition, but the script failed with a "matrix is not positive definite" error. This happened because the molecular graph has multiple disconnected components, making the Laplacian matrix singular (it has multiple zero eigenvalues).

Your task is to bypass the failing matrix decomposition by using an appropriate eigendecomposition or Singular Value Decomposition (SVD) to analyze the network correctly.

Please perform the following steps:
1. Read the undirected network edge list from `/home/user/network.edges`. The file contains space-separated node IDs (one edge per line).
2. Construct the unnormalized Laplacian matrix $L = D - A$ for this graph (where $D$ is the degree matrix and $A$ is the adjacency matrix). Ensure the matrix dimensions correspond to the maximum node ID present in the file, assuming node IDs start from 1. If a node ID between 1 and the maximum is completely disconnected (not in the file), it should still be represented as an isolated node in the matrix (row/column of all zeros).
3. Compute the eigenvalues of the Laplacian matrix.
4. Filter out the "zero" eigenvalues caused by the singular nature of the disconnected graph. (Treat any eigenvalue $< 10^{-7}$ as zero).
5. Fit a normal distribution to the remaining strictly *non-zero* eigenvalues. Specifically, calculate the sample mean and sample standard deviation (using $N-1$ degrees of freedom).
6. Write these fitted parameters to `/home/user/eigen_stats.txt` in the following exact format, rounding the numbers to exactly 4 decimal places:

```
Mean: <mean_value>
StdDev: <std_value>
```

You may use any programming language you prefer (e.g., Python, R) to write a script that performs this analysis.