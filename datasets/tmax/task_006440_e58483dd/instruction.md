You are acting as a data scientist analyzing a steady-state chemical kinetics model. You need to solve a system of non-linear equations for different parameter sets, manipulate the results into a multi-dimensional array, and compare them against a reference dataset.

For performance reasons, your team requires the numerical solver to be implemented in C/C++ and called from Python.

**The Model:**
The steady-state concentrations \( u \) and \( v \) (where \( u, v > 0 \)) depend on parameters \( p_1 \) and \( p_2 \) according to the following system of non-linear equations:
1. \( u^2 + p_1 v = 10 \)
2. \( p_2 u + v^2 = 10 \)

**Your Tasks:**
1. **Implement a Non-linear Solver in C++:**
   - Create a C++ file at `/home/user/solver.cpp`.
   - Implement a function with C linkage: `void solve_system(double p1, double p2, double* u_out, double* v_out)`.
   - Use the Newton-Raphson method to solve the system for \( u \) and \( v \).
   - Use an initial guess of \( u = 3.0 \), \( v = 3.0 \).
   - Run the solver for exactly 20 iterations (no early stopping required, just do 20 iterations to ensure convergence for this parameter space).
   - Compile this code into a shared library at `/home/user/solver.so` (e.g., using `g++ -shared -fPIC`).

2. **Generate the Solution Grid in Python:**
   - Write a Python script `/home/user/fit_model.py`.
   - Use `ctypes` to load `/home/user/solver.so` and call `solve_system`.
   - Create a 2D parameter grid for \( p_1 \) and \( p_2 \). Both parameters should take the 5 linearly spaced values: `[1.0, 2.0, 3.0, 4.0, 5.0]`.
   - Iterate over the grid to compute \( u \) and \( v \) for each of the 25 combinations of \( (p_1, p_2) \).
   - Store the computed concentrations in a 3-dimensional NumPy array of shape `(5, 5, 2)`, where the dimensions correspond to the indices of \( p_1 \), the indices of \( p_2 \), and the variables `(u, v)` respectively.

3. **Compare with Reference Dataset:**
   - A reference dataset exists at `/home/user/reference_data.csv`. It contains four columns with a header row: `p1, p2, u_ref, v_ref`.
   - The CSV rows correspond to the exact same parameter grid combinations.
   - Calculate the Sum of Squared Errors (SSE) between your computed 3D array and the reference data. The SSE is defined as the sum of \( (u - u_{ref})^2 + (v - v_{ref})^2 \) over all 25 parameter combinations.
   - Write the final SSE value to `/home/user/result_sse.txt`, formatted to exactly 4 decimal places (e.g., `0.1234`).

You may use standard Linux tools, `g++`, and Python 3 with `numpy` and `pandas`. Execute the necessary commands to compile the solver, run the Python script, and generate the final output file.