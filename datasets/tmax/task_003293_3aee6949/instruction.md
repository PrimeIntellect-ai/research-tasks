You are a performance engineer analyzing a numerical simulation of a non-linear limit cycle oscillator. The current solver exhibits divergence and inaccurate state distributions when the time-step is too large, but using an excessively small time-step causes performance bottlenecks. You need to profile the integration error to find the optimal time-step.

Your task is to write a Python script at `/home/user/perf_profile/analyze_step.py` that performs a convergence test.

Here are the specific requirements:
1. **The System**: Simulate an ensemble of 1000 independent particles following the 2D ODE:
   $$ \frac{dx}{dt} = y + x(1 - x^2 - y^2) $$
   $$ \frac{dy}{dt} = -x + y(1 - x^2 - y^2) $$
2. **Initial Conditions**: Generate the initial states $(x_0, y_0)$ for the 1000 particles using `numpy.random.default_rng(42).normal(0, 1, (1000, 2))`.
3. **Numerical Solver**: Implement the Forward Euler method to integrate the system from $t = 0$ to $t = 5.0$. You must vectorize the multi-dimensional array operations to compute the updates for all 1000 particles simultaneously.
4. **Convergence Testing**: Run the solver using the following sequence of time-steps (`dt`): `[0.2, 0.1, 0.05, 0.02, 0.01, 0.005, 0.001]`.
5. **Distance Metric**: Treat the final $x$-coordinates (at $t=5.0$) from the run with `dt = 0.001` as your high-fidelity "ground truth" reference distribution. For each of the other `dt` values, calculate the 1D Wasserstein distance between its final $x$-coordinates and the reference final $x$-coordinates (you may use `scipy.stats.wasserstein_distance`).
6. **Output**: Find the largest `dt` (from the list above, excluding 0.001) where the Wasserstein distance to the reference is strictly less than `0.05`. Write this single float value to the file `/home/user/perf_profile/optimal_dt.txt`.

Ensure the directory `/home/user/perf_profile` exists before writing to it. The final output file must contain only the optimal `dt` value as a decimal (e.g., `0.05`).