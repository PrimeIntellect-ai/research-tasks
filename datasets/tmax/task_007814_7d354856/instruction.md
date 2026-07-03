You are an operations-focused data scientist working on an embedded Linux system where Python and R are unavailable. You need to fit a parameter for an Ordinary Differential Equation (ODE) to experimental data using a Markov Chain Monte Carlo (MCMC) approach, relying exclusively on `bash` and `awk`.

An experimental dataset of radioactive decay is located at `/home/user/decay_data.tsv` (tab-separated, headers: `t` and `y`).

The system models the decay using a simple ODE:
dy/dt = -k * y

**Your Task:**
Write a bash script at `/home/user/fit_mcmc.sh` that uses `awk` to perform an MCMC estimation of the parameter `k`.

**Mathematical and Algorithmic Specifications:**
1. **ODE Numerical Solver:**
   Inside your MCMC evaluation, simulate the ODE using the Euler method.
   - Initial condition: `y = 100` at `t = 0`.
   - Step size: `dt = 1` (simulate exactly at the integer time steps `t=1` through `t=10`).
   - Formula: `y[t] = y[t-1] - k * y[t-1] * dt`

2. **Error Calculation:**
   Compare the simulated `y` against the true `y` from the dataset at `t=1, 2, ..., 10`.
   - Objective function: Sum of Squared Errors (SSE). `SSE = sum((y_sim - y_data)^2)`

3. **MCMC (Metropolis-Hastings) Setup:**
   - Seed `awk`'s random number generator in the BEGIN block using `srand(42)` (CRITICAL for deterministic verification).
   - Chain length: 1000 iterations.
   - Initial parameter guess: `k = 0.1`.
   - Proposal distribution: `k_new = k_current + (rand() - 0.5) * 0.1`
   - Acceptance criteria: 
     Calculate `SSE_new`.
     If `SSE_new < SSE_current`, accept the new `k` (`k_current = k_new`).
     If `SSE_new >= SSE_current`, calculate the acceptance probability `p = exp((SSE_current - SSE_new) / 100.0)`. Draw a random number `r = rand()`. If `r < p`, accept `k_new`. Otherwise, reject it (keep `k_current`).

4. **Outputs:**
   - For every iteration (1 to 1000), append the value of `k_current` at the end of the step to `/home/user/trace.txt`.
   - Calculate the mean of the `k` values from the **last 500 iterations** (burn-in period = 500, so average iterations 501 to 1000). Save this single floating-point mean value to `/home/user/k_mean.txt` (formatted with 4 decimal places, e.g., `printf "%.4f\n"`).

**Execution:**
Once the script `/home/user/fit_mcmc.sh` is created, make sure to execute it so that `/home/user/trace.txt` and `/home/user/k_mean.txt` are generated.