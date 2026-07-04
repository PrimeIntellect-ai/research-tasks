You are a machine learning engineer preparing training data. As part of a data cleaning pipeline, you need to filter out covariance matrices that are not numerically stable (i.e., not strictly positive definite) and compute a feature from the stable ones.

You have a dataset of 3x3 symmetric matrices stored in `/home/user/matrices.txt`. Each line contains 9 space-separated floating-point numbers representing the matrix in row-major order.

Your task:
1. Write a C++ program at `/home/user/process_matrices.cpp` that reads `/home/user/matrices.txt`.
2. For each matrix, attempt to compute its Cholesky decomposition $A = L L^T$, where $L$ is a lower triangular matrix.
3. A matrix is considered "Unstable" if, during the Cholesky decomposition, the argument to any square root is less than or equal to `1e-6`.
4. If the matrix is stable, compute the sum of all 9 elements of $L$ (including the zeros in the upper triangle).
5. The program should write its results to `/home/user/stable_log.txt`.
   - For a stable matrix, write `Stable: <sum>`, where `<sum>` is formatted to exactly 2 decimal places.
   - For an unstable matrix, write `Unstable`.
   - Maintain the same order as the input file, one result per line.
6. Compile your program (e.g., using `g++`) and run it to produce the output file. 

You must only use standard C++ libraries (no external libraries like Eigen).