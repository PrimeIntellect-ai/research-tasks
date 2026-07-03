I am a data scientist building a reproducible modeling pipeline. Before I trust my numerical solvers on complex data, I need to validate them against known analytical solutions.

Please create a Rust project to solve a simple exponential decay ODE and compute its error against the analytical solution. 

Here are your instructions:
1. Initialize a new Rust binary project at `/home/user/ode_validator`.
2. Write a Rust program that numerically solves the Ordinary Differential Equation (ODE):
   `dy/dt = -0.5 * y`
   with the initial condition `y(0) = 1.0`.
3. Use the **Forward Euler method** to solve this ODE from `t = 0.0` to `t = 10.0` (inclusive) with a time step of `dt = 0.1`.
4. At each time step, calculate the absolute error between the numerical solution and the exact analytical solution. The analytical solution is `y(t) = exp(-0.5 * t)`.
5. Find the maximum absolute error across all time steps (from `t=0.0` to `t=10.0`).
6. The program must write ONLY this maximum absolute error formatted to exactly 6 decimal places (e.g., `0.024681`) to a file at `/home/user/max_error.txt`.
7. Build and run your Rust program to generate the output file. You may only use the Rust standard library (no external crates are needed).

Ensure that `/home/user/max_error.txt` exists and contains only the requested number upon completion.