I am a performance engineer profiling a C++ application that simulates a 1D physical system. The simulation calculates the total energy (heat) of the system at each time step. However, due to the large size of the grid and the use of single-precision `float`, the naive reduction loop suffers from severe floating-point precision loss (catastrophic cancellation/truncation). This causes our simulation to fail convergence checks against our reference dataset. 

Additionally, the simulation loads a 4x4 boundary condition matrix. We need to compute its determinant using LU decomposition to verify system stability, but this feature is currently unimplemented.

Your tasks are:
1. Fix the precision issue in `/home/user/sim/pde_solver.cpp`. Modify the `compute_total_heat` function to use **Kahan summation** so that the reduction is numerically stable and deterministic, even for millions of single-precision floats.
2. Implement the `compute_determinant_lu` function in the same file. It must perform an LU decomposition (without pivoting is acceptable for this matrix) on the 4x4 matrix loaded from `/home/user/sim/matrix.txt`, and return the determinant.
3. Compile the C++ program (`g++ -O3 pde_solver.cpp -o pde_solver`).
4. Run the program. It will simulate a number of steps and then print a final report.
5. Save the exact final report printed by the program to `/home/user/sim/result.log`.

The output written to `/home/user/sim/result.log` must exactly follow this format:
```
Total Heat: <value>
Determinant: <value>
```

Constraints:
* Do not change the data types of the grid from `float` to `double`. The memory overhead is too large in production. You must fix the issue algorithmically via Kahan summation.
* Do not use external libraries (like Eigen or LAPACK) for the LU decomposition. Write a simple, self-contained LU decomposition for the 4x4 `std::vector<std::vector<float>>`.