You are acting as a performance engineer optimizing a numerical simulation. 

We have a Python script located at `/home/user/run_diffusion.py` that simulates a diffusion process on a network (graph) over time using an ordinary differential equation (ODE) solver. The ODE models a system that rapidly diffuses toward a steady state. 

Currently, the script is experiencing major performance issues:
1. The numerical integrator is extremely slow. It diverges or takes excessively small steps due to wrong step-size adaptation because the underlying ODE system is "stiff," but the script uses the default explicit Runge-Kutta method (`RK45`).
2. The script contains a placeholder for parallel computing but currently processes the graphs sequentially in a loop.
3. It lacks analytical solution validation.

Your task is to fix and optimize `/home/user/run_diffusion.py` with the following requirements:
1. **Fix the Integrator:** Change the `solve_ivp` method to an appropriate solver for stiff equations (such as `BDF` or `LSODA`) so it completes quickly.
2. **Parallelize:** Use Python's `multiprocessing.Pool` with 4 workers to run the `simulate_graph` function over the `seeds` list `[1, 2, 3, 4]` concurrently, instead of a simple `for` loop.
3. **Analytical Validation:** For each graph, the analytical steady-state solution of this specific diffusion process implies that all nodes converge to the exact mean of the initial conditions (`x0.mean()`). Add a validation step inside `simulate_graph` that `assert`s the absolute difference between the numerical mean at the final time (`final_x.mean()`) and the analytical mean (`x0.mean()`) is less than `1e-5`.
4. **Output:** The script must write the analytical means to `/home/user/steady_states.json` as a JSON dictionary mapping the seed (as a string, e.g., `"1"`) to its corresponding analytical mean.

Run the script to verify it works, completes rapidly, and produces the correct output file.