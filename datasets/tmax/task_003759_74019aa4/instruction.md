You are a machine learning engineer building a reproducible pipeline to prepare graph training data for a neural network. We encountered issues with near-singular matrices during graph convolution operations. To fix this, we need to apply ridge regularization to our graph Laplacian matrices.

Your task is to write a Bash shell script `/home/user/normalize_graph.sh` that processes a square adjacency matrix representing a molecular graph network and outputs the regularized graph Laplacian matrix.

Requirements:
1. The script must accept a square adjacency matrix from standard input (stdin). The matrix will be provided as space-separated non-negative integers, one row per line.
2. The script must compute the unnormalized graph Laplacian $L = D - A$, where $D$ is the degree matrix (a diagonal matrix where $D_{ii}$ is the sum of the $i$-th row of $A$) and $A$ is the adjacency matrix.
3. To prevent singular matrix issues, add a constant ridge regularization parameter $\lambda$ to the diagonal of the Laplacian. The regularized matrix $L_{reg}$ is defined as $L + \lambda I$, where $I$ is the identity matrix.
4. The value for the parameter $\lambda$ is documented in an image file located at `/app/settings.png`. You will need to extract the correct integer value for $\lambda$ from this image. (You may use OCR tools like `tesseract` which are available on the system).
5. The output must be printed to standard output (stdout) as space-separated integers, one row per line, matching the dimensions of the input matrix.
6. Use standard bash tools (e.g., `awk`, `sed`, `grep`, `bash` built-ins). Do not use Python, R, or compiled languages to process the matrix.
7. Make sure your script is executable (`chmod +x /home/user/normalize_graph.sh`).

For example, if the input adjacency matrix is:
```
0 1 1
1 0 0
1 0 0
```
And if $\lambda$ was 5, the degree matrix $D$ would have diagonal `[2, 1, 1]`. The Laplacian $L$ would be:
```
 2 -1 -1
-1  1  0
-1  0  1
```
Adding $\lambda=5$ to the diagonal gives:
```
 7 -1 -1
-1  6  0
-1  0  6
```

Ensure your script works for any square matrix dimensions up to 50x50 and strictly matches this logic. An automated testing suite will evaluate your script against thousands of random matrices to ensure bit-exact output equivalence with our reference implementation.