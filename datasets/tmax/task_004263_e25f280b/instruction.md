You are helping a researcher organize and search through a large dataset of embedding vectors. The researcher has a reference similarity search implementation at `/app/ref_search` (a stripped binary) that takes a dataset of vectors and a set of query vectors, and outputs the top 10 nearest neighbors (using Euclidean distance) for each query.

However, `/app/ref_search` is a naive implementation and is too slow for production benchmarking. 

Your task is to:
1. Understand the I/O format of the embeddings. The dataset `/home/user/dataset.bin` contains 10,000 vectors, and `/home/user/queries.bin` contains 100 query vectors. Both are flat binary files consisting of 32-bit floating-point numbers (little-endian, row-major format). The dimensionality of the vectors is 128.
2. Write a highly optimized C++ program `/home/user/fast_search.cpp` that produces the exact same output as `/app/ref_search dataset.bin queries.bin`.
   - Your program must accept two arguments: `<dataset_path> <queries_path>`.
   - For each query, it should print the 10 integer indices (0-based) of the closest dataset vectors, separated by spaces. Print one line per query.
   - Hint: Use linear algebra (e.g., matrix multiplication expansion of the Euclidean distance formula: $||x - y||^2 = ||x||^2 + ||y||^2 - 2x^T y$) and libraries like Eigen (available via `apt-get install libeigen-dev`) to maximize inference performance.
3. Compile your program to `/home/user/fast_search` (e.g., using `-O3 -march=native -I/usr/include/eigen3`).
4. Write a script `/home/user/benchmark.py` that runs both `/app/ref_search` and your `fast_search` 15 times each, measures the execution time of each run, and performs hypothesis testing. Specifically, calculate the 95% confidence interval for the mean speedup ratio (`time_ref / time_fast`). Write the lower and upper bounds of this confidence interval to `/home/user/ci.txt` as two comma-separated floats (e.g., `12.45, 14.21`).

An automated verifier will test your `/home/user/fast_search` binary against a secret hold-out dataset to ensure it achieves a strict metric threshold for inference performance speedup compared to `/app/ref_search`, while maintaining 100% identical recommendations.