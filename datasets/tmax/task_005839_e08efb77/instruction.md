You are a machine learning engineer preparing graph-based training data for a new model. The model requires the Cholesky decomposition of a modified Graph Laplacian matrix to extract node features. However, the standard Graph Laplacian is positive semi-definite (it has a zero eigenvalue for the connected components), which causes the standard Cholesky factorization to fail due to singularity.

Your task is to write a C++ program that constructs this matrix, applies a small regularization to make it positive definite, computes the Cholesky decomposition, and validates the output.

Here are the requirements:
1. Create a C++ program at `/home/user/prepare_data.cpp`.
2. The program should construct the Laplacian matrix of a 1D Ring Graph (cycle graph) with exactly $N = 2000$ nodes. 
   - Nodes are connected to their immediate neighbors (node `i` is connected to `i-1` and `i+1`, with node `0` connected to `N-1`).
   - The Laplacian is $L = D - A$, where $D$ is the degree matrix and $A$ is the adjacency matrix.
3. Use OpenMP to parallelize the construction of the dense Laplacian matrix. 
4. Apply a regularization term $\epsilon = 1e-3$ by adding $\epsilon I$ to the Laplacian, resulting in $M = L + \epsilon I$.
5. Compute the Cholesky decomposition $M = C C^T$ (where $C$ is a lower triangular matrix). You must use the Eigen C++ library for this (you can download the Eigen headers to `/home/user/eigen` and include them).
6. Validate the analytical correctness by calculating the L2 norm (Euclidean norm) of the diagonal elements of the resulting lower triangular matrix $C$.
7. Write the computed L2 norm of the diagonal of $C$ to a file named `/home/user/validation.log` in plain text (formatted to 6 decimal places).

You should write a bash script `/home/user/run.sh` that:
- Downloads and extracts the Eigen library (version 3.4.0) to `/home/user/eigen`.
- Compiles `prepare_data.cpp` with OpenMP enabled (e.g., using `g++ -O3 -fopenmp -I/home/user/eigen`).
- Executes the compiled program to produce `/home/user/validation.log`.

Ensure that the output in `validation.log` contains only the numeric value of the L2 norm.