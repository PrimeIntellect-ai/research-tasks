You are a performance engineer tasked with creating a synthetic benchmark pipeline named "SpectroMark" to profile an HPC system's capability in handling experimental spectroscopy data.

Your objective is to implement a C++ pipeline that simulates, stores, and processes spectral data, and then profile its execution. 

Follow these requirements strictly:

1. **Environment Setup**: 
   Install necessary packages for C++ development, HDF5 (C/C++ bindings), Eigen3 (for matrix operations), Valgrind (for profiling), and Python3 with matplotlib and h5py (for visualization). Use `apt-get` for system packages and `pip` for Python packages where appropriate.

2. **C++ Implementation (`/home/user/spectromark.cpp`)**:
   Write a C++ program that performs the following steps sequentially:
   * **Monte Carlo Generation**: Generate a 1000 (rows/events) by 500 (columns/bins) matrix of `double` precision spectral data. 
     * Use `std::mt19937` with a fixed seed of `42`.
     * The value at row `i` and column `j` should be: $A_{i,j} = \sin(j \times 0.05) + N$, where $N$ is a random value sampled from a uniform distribution between $0.0$ and $0.1$ using `std::uniform_real_distribution<double>(0.0, 0.1)`.
   * **HDF5 I/O**: Write this 1000x500 matrix to an HDF5 file at `/home/user/spectra.h5` in a dataset named `raw_data`. Then, read the matrix back from the file into memory.
   * **Matrix Decomposition**: Using the Eigen3 library, perform a Singular Value Decomposition (SVD) on the loaded matrix to extract the singular values.
   * **Output**: Save exactly the top 5 largest singular values (in descending order, one per line, formatted to 4 decimal places) to `/home/user/svd_results.txt`.

3. **Compilation and Profiling**:
   * Compile the C++ program into an executable at `/home/user/spectromark`. Ensure you link against the necessary HDF5 libraries and include Eigen3 headers. Use optimization flag `-O2` and debug flag `-g`.
   * Profile the executable using Valgrind's Callgrind tool. Save the callgrind output to `/home/user/callgrind.out` (use `--callgrind-out-file=/home/user/callgrind.out`).

4. **Visualization (`/home/user/plot_svd.py`)**:
   * Write a Python script that reads `/home/user/svd_results.txt`.
   * It must generate a bar chart of the 5 singular values and save the plot as a PNG image to `/home/user/svd_plot.png`.

Execute all necessary commands to build, run, profile, and visualize the benchmark.