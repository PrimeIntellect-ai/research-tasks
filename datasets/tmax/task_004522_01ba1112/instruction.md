You are helping a researcher port a legacy simulation component into a modern Python pipeline. 

The researcher has a compiled, stripped legacy binary located at `/app/bin/legacy_solver`. This tool reads a sequence of linear systems ($Ax = b$) from an HDF5 file, solves them, and writes the solutions ($x$) to an output HDF5 file. 

The binary is known to perform matrix decomposition to solve the systems, but it employs a specific, undocumented regularization or filtering technique to handle near-singular matrices without failing. 

Your task is to:
1. Reverse-engineer or deduce the mathematical logic of the legacy solver by experimenting with it. You can generate custom HDF5 files using Python, feed them to the binary, and analyze its outputs to figure out exactly how it handles small or near-zero eigenvalues/singular values.
2. Write a Python script at `/home/user/custom_solver.py` that perfectly replicates the binary's behavior. 

**I/O Specifications:**
- Both the legacy binary and your Python script must accept exactly two command-line arguments: `<input_file.h5> <output_file.h5>`
- The input HDF5 file contains groups named `system_0`, `system_1`, ..., `system_N`.
- Inside each group, there are two datasets:
  - `A`: A 2D float64 numpy array (an $N \times N$ matrix).
  - `b`: A 1D float64 numpy array (a vector of length $N$).
- The output HDF5 file must contain groups with the same names (`system_0`, `system_1`, etc.).
- Inside each output group, there must be a single dataset `x`, which is the 1D float64 array representing the solution.

Write `/home/user/custom_solver.py` so that it uses `h5py` and `numpy`/`scipy` to replicate the legacy solver's exact mathematical outputs. You can find some sample input data to play with at `/home/user/sample_inputs.h5`.