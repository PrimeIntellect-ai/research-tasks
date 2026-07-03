You are a performance engineer tasked with optimizing a numerical simulation. The simulation currently models a specific chemical reaction system but is suffering from severe performance issues due to numerical instability when using standard explicit ODE solvers. 

Your task is to extract the simulation parameters from an observational data log, write a numerically stable Python solver for the system, profile its performance, and output the final state.

1. **Observational Data Reshaping**:
   You have been provided with an unstructured log file at `/home/user/measurements.txt`. The file contains various measurements. Extract the exact values for the initial conditions (`y0`, `y1`), the parameter `mu`, and the end time `t_end`.

2. **ODE Numerical Solving & Stability**:
   The system of ordinary differential equations (ODEs) is defined as:
   `dy0/dt = -mu * y0 + mu * y1`
   `dy1/dt = y0 - y1`
   
   Write a Python script at `/home/user/optimize.py` that solves this initial value problem from `t = 0` to `t = t_end`. You must use `scipy.integrate.solve_ivp` with a solver method appropriate for **stiff** ODEs to ensure numerical stability and good performance. Set the tolerances to `rtol=1e-8` and `atol=1e-10`.

3. **Profiling**:
   In your script, wrap the ODE solving step with Python's built-in `cProfile` module. Export the profiling statistics to a binary file located at `/home/user/profile.out` using `dump_stats()`.

4. **Output**:
   After solving, extract the final values of `y0` and `y1` at `t_end`. Write these values to `/home/user/final_state.json` in the exact following format, with the values rounded to 5 decimal places:
   `{"y0": 0.00000, "y1": 0.00000}` (Replace the zeros with your computed rounded values).

Ensure all files are saved in `/home/user/` and that your script `optimize.py` executes successfully.