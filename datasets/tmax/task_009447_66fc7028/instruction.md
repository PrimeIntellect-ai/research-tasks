You are acting as a performance engineer tasked with testing the numerical convergence, statistical accuracy, and parallel scalability of a stochastic simulation.

Your goal is to implement a Monte Carlo simulation of Geometric Brownian Motion (GBM) in Rust, verify its strong convergence using the Kolmogorov-Smirnov (KS) distance metric, and profile its parallel execution.

**Mathematical Background:**
We are simulating the Stochastic Differential Equation (SDE):
$$dX_t = \mu X_t dt + \sigma X_t dW_t$$
where $X_0 = 1.0$, $\mu = 0.05$, $\sigma = 0.2$, and $T = 1.0$.
The theoretical distribution of $X_T$ is Lognormal, such that $\ln(X_T) \sim \mathcal{N}((\mu - \sigma^2/2)T, \sigma^2 T)$.

**Step 1: Implement the Rust Simulation**
Create a new Rust project at `/home/user/gbm_sim`.
Write a CLI program that takes two arguments: `N` (number of paths) and `dt` (time step size).
The program must:
1. Use the Euler-Maruyama method to simulate `N` independent paths from $t=0$ to $t=T$ with step size `dt`.
2. Use the `rayon` crate to parallelize the simulation of the `N` paths.
3. Compute the empirical CDF of the final values $X_T$.
4. Calculate the Kolmogorov-Smirnov (KS) distance between the empirical distribution of $X_T$ and the theoretical Lognormal distribution. You may use the `statrs` crate for the theoretical distribution.
5. Output the KS distance to `stdout` as a single floating-point number.

**Step 2: Convergence Testing**
Write a bash script at `/home/user/run_convergence.sh` that:
1. Builds the Rust project in release mode.
2. Runs the simulation with `N=500000` for three different `dt` values: `0.1`, `0.01`, and `0.001`.
3. Appends the results to `/home/user/convergence.log` in the exact format: `<dt>,<KS_distance>` (one per line).

**Step 3: Parallel Profiling**
Write a bash script at `/home/user/profile_parallel.sh` that:
1. Runs the simulation for `N=2000000` and `dt=0.001`.
2. Runs it first with the environment variable `RAYON_NUM_THREADS=1`.
3. Runs it second with `RAYON_NUM_THREADS=4`.
4. Measures the execution time for both runs.
5. Writes the execution times to `/home/user/profile.log` in the exact format:
```
threads=1,time=<time_in_seconds>
threads=4,time=<time_in_seconds>
```

Execute both scripts so the log files are generated and the system state is finalized.