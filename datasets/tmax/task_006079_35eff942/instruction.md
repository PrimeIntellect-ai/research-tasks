You are an assistant helping a computational physics researcher. 

You have been provided with the source code for a 1D heat diffusion simulation in C++ located at `/home/user/heat_sim.cpp`. The simulation models heat transferring across a 1D rod of length $L=1.0$ from $t=0$ to $t=0.5$. The code uses an explicit Forward Time-Centered Space (FTCS) finite difference scheme.

The executable will take three command-line arguments:
1. `N`: The number of spatial intervals (mesh refinement).
2. `M`: The number of time steps.
3. `alpha`: The thermal diffusivity coefficient.

We have an experimental reference dataset located at `/home/user/reference.csv` that contains the exact temperature profile of the rod at $t=0.5$ at high resolution.

Your objectives:
1. **Compilation**: Compile `/home/user/heat_sim.cpp` into an executable named `heat_sim` in the user's home directory.
2. **Curve Fitting & Regression**: The exact value of `alpha` is unknown, but it is a multiple of 0.01 between `0.01` and `0.10`. Compare the simulation outputs to `reference.csv` to determine the correct `alpha` that minimizes the mean squared error.
3. **Numerical Stability**: The FTCS scheme suffers from numerical instability if the time step and spatial step are not properly balanced. Determine the stability condition for this scheme and ensure your chosen parameters remain strictly stable.
4. **Mesh Refinement**: Find the **minimum integer** `N` (where $N \ge 10$) and the **minimum integer** `M` (that satisfies the stability condition for your `N` and `alpha`) such that the **Maximum Absolute Error** between the simulation output and the interpolated reference data at the corresponding spatial points is strictly less than `0.005`.

Once you have identified the optimal values, write them to `/home/user/solution.txt` as a single, comma-separated line in the exact format:
`alpha,N,M`
(e.g., `0.03,15,45`)