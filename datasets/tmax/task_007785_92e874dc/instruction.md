You are a performance engineer profiling a bioinformatics application that models bacterial population growth. The application solves a non-linear Ordinary Differential Equation (ODE) but is currently running slower than expected. You want to compare the performance and accuracy of two different numerical solvers.

Write a Python script at `/home/user/profile_ode.py` that does the following:

1. Defines the Logistic Growth ODE: $dy/dt = r y (1 - y/K)$, where growth rate $r = 1.5$ and carrying capacity $K = 100.0$.
2. Sets the initial condition $y(0) = 1.0$, the time span from $t = 0$ to $t = 15$, and evaluates the solution at 300 evenly spaced points from $t = 0$ to $t = 15$ (inclusive).
3. Profiles two `scipy.integrate.solve_ivp` solvers: `'RK45'` and `'Radau'`.
4. For each solver, run the integration 50 times. Record the execution time of each run using `time.perf_counter()`.
5. Performs an independent two-sample Welch's t-test (using `scipy.stats.ttest_ind` with `equal_var=False`) to compare the execution times of the RK45 runs vs the Radau runs.
6. Computes the 1D Wasserstein distance (using `scipy.stats.wasserstein_distance`) between the evaluated $y$ values of the *first* run of RK45 and the *first* run of Radau.
7. Saves the results to a JSON file at `/home/user/profile_results.json` with the following keys:
   - `"t_stat"`: the calculated t-statistic (float)
   - `"p_value"`: the calculated p-value (float)
   - `"wasserstein_dist"`: the calculated Wasserstein distance between the two solution arrays (float)

Finally, execute your script so the JSON file is generated. Ensure that any necessary Python packages (like `scipy` and `numpy`) are used correctly.