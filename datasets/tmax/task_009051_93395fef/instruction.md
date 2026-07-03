You are a Performance Engineer optimizing a scientific data processing pipeline. Your team has a theoretical algorithm for processing noisy sensor data, but it needs to be implemented efficiently in C++ using parallelization and linear algebra libraries.

Your objective is to write, compile, and execute a C++ application that performs a specific sequence of numerical operations on an HDF5 dataset, parallelizes the independent loops, and validates the output against a reference dataset.

### Problem Specification
1. **Input Data**: You are provided with an HDF5 file at `/home/user/input_data.h5`. It contains a single 2D dataset named `/raw_signals` of type 64-bit float (double). The matrix $A$ has dimensions $N \times M$ (where $N$ is the number of signals/rows, and $M$ is the number of time steps/columns). 
2. **Numerical Differentiation**: For each signal (row) in $A$, compute the first derivative with respect to time to create a new matrix $D$. Use the central difference method for interior points: $D_{i,j} = \frac{A_{i,j+1} - A_{i,j-1}}{2 \Delta t}$. For the boundary points, use the forward difference for $j=0$ and backward difference for $j=M-1$. The time step is $\Delta t = 0.01$.
3. **Signal Filtering via SVD**: Treat $D$ as a dense matrix. Perform a Singular Value Decomposition (SVD) on $D$. Reconstruct a filtered derivative matrix $D_{filtered}$ using only the top $K=5$ singular values (set all other singular values to zero). You must use the Eigen C++ library for this matrix decomposition.
4. **Numerical Integration**: For each filtered signal (row) in $D_{filtered}$, compute the definite integral over the entire time domain using the Trapezoidal rule (with $\Delta t = 0.01$). This will yield a 1D vector $I$ of length $N$ containing the integrated values.
5. **Parallelization**: You must use OpenMP to parallelize the numerical differentiation and integration steps across the $N$ signals. Use 4 OpenMP threads.
6. **Validation**: Read the reference dataset from `/home/user/reference.csv`, which contains $N$ expected integral values (one per line, as floats). Compute the Maximum Absolute Error (MAE) between your computed vector $I$ and the reference dataset.

### Implementation Constraints
* Write your C++ code in `/home/user/process_signals.cpp`.
* You must use the HighFive library or the standard C/C++ HDF5 API for reading the data. The HDF5 development libraries (`libhdf5-dev`) and Eigen3 (`libeigen-dev`) are available in the system.
* Compile your code into an executable at `/home/user/process_signals`. Ensure you link the necessary HDF5 libraries and enable OpenMP.
* Run your executable. The executable should generate a JSON file at `/home/user/profiling_results.json` with exactly the following format:
```json
{
  "max_absolute_error": <float_value>,
  "num_threads_used": 4
}
```

Do not use external programs (like Python or MATLAB) to perform the math; the logic must be implemented in your C++ code. You may use shell commands to explore the data, install user-level dependencies if needed, and compile the code.