You are an ML Engineer preparing training data for a generative model. Part of your pipeline involves processing a set of covariance matrices. Unfortunately, one of the input matrices is near-singular, causing downstream Cholesky decompositions to fail. 

To fix this, you need to write a C++ program that applies a Monte Carlo regularization technique to the matrix.

An HDF5 file is located at `/home/user/data/input.h5` containing a single 10x10 dataset named `cov_matrix` of type double.

Write a C++ program at `/home/user/regularize.cpp` that does the following:
1. Reads the `cov_matrix` dataset from `/home/user/data/input.h5`.
2. Performs a Monte Carlo simulation with $N=10000$ iterations. In each iteration:
   - Generate a 10x10 diagonal matrix where each diagonal element is independently sampled from a Uniform distribution $\mathcal{U}(0, 0.01)$.
   - Add this random diagonal matrix to the original `cov_matrix`.
   - Record the trace of this new regularized matrix.
3. Compute the mean regularized matrix across all 10000 iterations.
4. Save this mean matrix to a new HDF5 file `/home/user/data/output.h5` in a dataset named `reg_matrix`.
5. Calculate the 95% bootstrap confidence interval (the 2.5th and 97.5th percentiles) of the 10000 trace values recorded.
6. Write these two values (lower bound, upper bound) comma-separated to `/home/user/data/trace_ci.txt`.

Requirements:
- Use the standard HDF5 C++ API (`#include <H5Cpp.h>`). 
- A Makefile is not provided; you must compile your code manually using `g++` and the appropriate HDF5 flags (e.g., `-lhdf5_cpp -lhdf5`).
- Ensure the output matrix is saved as an HDF5 dataset of type double.
- The random number generator should be seeded with the value `42` (`std::mt19937 gen(42);`) to ensure reproducibility.

Please create the C++ script, compile it, and run it to produce the required outputs.