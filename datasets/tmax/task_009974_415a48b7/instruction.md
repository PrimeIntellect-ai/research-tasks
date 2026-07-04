I am running some simulations of a linear dynamical system and need help testing the numerical stability of a custom C integrator against an exact analytical solution.

I have written a C file at `/home/user/sim_project/integrator.c` that implements a 4th-order Runge-Kutta (RK4) integrator.

Your tasks:
1. **Compile the C code**: Compile `/home/user/sim_project/integrator.c` into a shared library named `/home/user/sim_project/libintegrator.so`.
2. **Write a Python script**: Create `/home/user/sim_project/run_sim.py` that does the following:
   - Uses `ctypes` to load `libintegrator.so`.
   - Defines the linear ODE system $\frac{dx}{dt} = A x$ where the matrix $A = \begin{bmatrix} -100 & 1 \\ 0 & -1 \end{bmatrix}$. The initial condition is $x(0) = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$.
   - Computes the **exact** solution at $t = 1.0$ using matrix decomposition (e.g., eigendecomposition) or the matrix exponential.
   - Uses the C library's `integrate` function to numerically solve the system from $t=0$ to $t=1.0$ for three different time steps (`dt`): `0.1`, `0.01`, and `0.001`.
   - For each `dt`, calculates the L2 norm of the error (Euclidean distance) between the RK4 solution at $t=1.0$ and the exact solution at $t=1.0$.
3. **Log the results**: Save the L2 error for each `dt` in a JSON file at `/home/user/sim_project/results.json`. The JSON should have the exact format:
```json
{
  "error_dt_0.1": <float>,
  "error_dt_0.01": <float>,
  "error_dt_0.001": <float>
}
```

Ensure your Python script is executable and runs without errors. I will verify the task by checking the contents of `/home/user/sim_project/results.json`.