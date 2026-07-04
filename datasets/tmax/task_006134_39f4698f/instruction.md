You are acting as a data scientist modeling a chemical reaction network. I need you to perform the following steps to compile our network generation tool, integrate the resulting ODEs, and determine the system's convergence time.

1. **Compile the Network Generator**: 
   There is a C source file located at `/home/user/network_gen.c`. Compile it using `gcc` into an executable named `/home/user/network_gen`.

2. **Generate the Network**:
   Run `/home/user/network_gen`. This will create a file named `/home/user/network.csv` in the current directory, representing a transition rate matrix `R` for our chemical network graph.

3. **Numerical Integration and Convergence Testing**:
   Write and execute a Python script at `/home/user/model_fit.py` that does the following:
   - Loads the matrix `R` from `/home/user/network.csv`.
   - Sets up a system of ordinary differential equations: `dx/dt = R @ x` (where `@` is matrix multiplication).
   - Uses `scipy.integrate.solve_ivp` to integrate the system from `t = 0` to `t = 200`.
   - Uses the initial condition `x0 = [1000.0, 0.0, 0.0, 0.0]`.
   - Evaluates the derivative `dx/dt` at discrete time steps `t = 0.0, 0.1, 0.2, 0.3, ...` (step size of exactly 0.1).
   - Finds the *first* time `t` (from that discrete set of evaluated times) where the maximum absolute derivative across all nodes is strictly less than `0.1`. In other words, `max(abs(dx/dt)) < 0.1`.
   
4. **Log the Output**:
   Write the convergence time `t` you found to `/home/user/convergence_time.txt`, formatted to exactly one decimal place (e.g., `42.5`).

Ensure your Python script relies on `scipy` and `numpy`.