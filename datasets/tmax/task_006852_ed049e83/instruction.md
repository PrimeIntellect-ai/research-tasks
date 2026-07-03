A researcher needs you to compute the sample covariance matrix of a combined dataset stored across multiple binary files. 

You are given two binary files, `/home/user/data_A.bin` and `/home/user/data_B.bin`. Both contain 32-bit floating-point numbers (IEEE 754 single precision) stored in row-major order.
- `/home/user/data_A.bin` contains 100,000 rows and 3 columns.
- `/home/user/data_B.bin` contains 100,000 rows and 2 columns.
The rows in both files correspond to the same observations (e.g., row $i$ in A and row $i$ in B represent the same sample's features).

Your task is to:
1. Write a C++ program at `/home/user/compute_cov.cpp` that joins the two datasets into a single 100,000 $\times$ 5 conceptual dataset.
2. Compute the $5 \times 5$ sample covariance matrix (using $N-1$ for the unbiased estimator) of this combined dataset. The columns of A are features 0, 1, 2, and the columns of B are features 3, 4.
3. Write the resulting $5 \times 5$ covariance matrix to a binary file at `/home/user/cov_matrix.bin` as 32-bit floats in row-major order (exactly 25 float values, 100 bytes).

Requirements:
- The program must be written in C++.
- You should compile it using standard tools, e.g., `g++ -O3 /home/user/compute_cov.cpp -o /home/user/compute_cov`.
- Ensure you run the compiled executable to produce the output file.