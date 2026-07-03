You are an AI assistant helping a bioinformatics analyst model the spatial spread of an advantageous genetic mutation across a 1D sequence of subpopulations. We are modeling this using the Fisher-KPP reaction-diffusion equation.

I have written a C++ simulation script located at `/home/user/fisher_sim.cpp`. However, the numerical integrator diverges and produces `NaN` values because the explicit step-size adaptation is incorrect for the grid resolution.

Your task is to fix the simulation, parallelize it, and perform a statistical analysis on the output.

**Step 1: Fix and Refine the Simulation (`/home/user/fisher_sim.cpp`)**
1. **Mesh Refinement:** The current domain uses a coarse grid of $N=100$ points. Refine the spatial mesh by changing this to $N=1000$ points.
2. **Step-size Adaptation:** The explicit Euler integration diverges because the time step `dt` violates the Courant–Friedrichs–Lewy (CFL) stability condition for diffusion. Update the calculation of `dt` in the code to be exactly `0.4 * (dx * dx) / D`. Keep the calculation for `steps = std::ceil(T / dt)` the same.
3. **Parallel Computing:** Parallelize the spatial update loop (the inner loop iterating over `1` to `N-1`) using OpenMP.
4. Compile the fixed C++ code with OpenMP support (use `g++`) and run it. It should generate a file named `final_state.txt` containing space-separated `x` and `u` values.

**Step 2: Statistical Analysis (`/home/user/analyze.py`)**
1. Write a Python script at `/home/user/analyze.py` that reads `final_state.txt`.
2. Filter the data to only include positions where $0.2 \le x \le 0.8$.
3. Perform a linear regression (predicting $u$ from $x$) on this filtered subset to find the linear trend of the mutation concentration in the middle of the domain.
4. Write the results of the linear regression to `/home/user/regression_results.txt` in exactly the following format (round to 6 decimal places):
```
Slope: <value>
Intercept: <value>
```

Run your Python script to generate the final results. I will grade your success based on the correctness of `/home/user/regression_results.txt`.