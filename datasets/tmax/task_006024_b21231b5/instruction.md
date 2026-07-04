You are a bioinformatics analyst working on modeling the GC-content drift of a viral genome over time. You have observed the sequence's GC-content at different time points and need to fit a kinetic model, solve for an underlying structural factor, perform Bayesian parameter estimation via MCMC, and write regression tests for your code.

The observation data is located at `/home/user/observations.csv` (which you will need to assume exists, formatted with headers `time,gc_content`).

Your task is to create a Python file `/home/user/analyze.py`, a test file `/home/user/test_analyze.py`, and a shell script `/home/user/run_pipeline.sh` that fulfill the following requirements:

1. **Optimization**:
   In `analyze.py`, write a function `optimize_params(times, gcs)` that takes numpy arrays of time and GC-content. 
   Fit the nonlinear model: $GC(t) = C + (GC_0 - C) e^{-k t}$
   where $GC_0$ is the first observed GC-content (at $t=0$). Use `scipy.optimize.curve_fit` to find the optimal steady-state GC-content $C$ and the decay rate $k$. Return a tuple `(C, k)`.

2. **Nonlinear Equation Solving**:
   Write a function `solve_structural_factor(C)` that solves the implicit nonlinear equation $x^3 + 2x - C = 0$ for $x$. This represents a simplified sequence structural stability factor. Use `scipy.optimize.fsolve` or `root`. Return the float value of $x$.

3. **MCMC Sampling**:
   Write a function `mcmc_sample(times, gcs, steps=10000, seed=42)` to estimate the posterior means of $C$ and $k$.
   - **Likelihood**: Assume $GC_{obs}(t) \sim \text{Normal}(\mu(t), \sigma^2)$, where $\mu(t) = C + (GC_0 - C) e^{-k t}$ and $\sigma = 0.02$.
   - **Priors**: Uniform prior for $C \in [0, 1]$, Uniform prior for $k \in [0, 5]$.
   - **Proposal**: Normal distribution centered on the current parameter with standard deviation $0.05$ for both parameters. Draw the proposal for $C$, then for $k$.
   - **Initialization**: Start at $C=0.5, k=1.0$. Use `numpy.random.seed(seed)`.
   - **Burn-in**: Run for `steps` iterations, discard the first 5000 samples.
   - Return the tuple `(mean_C, mean_k)` of the remaining samples.

4. **Regression Testing**:
   Create `/home/user/test_analyze.py` using `pytest`. Write at least two tests:
   - `test_solve_structural()`: Verify that `solve_structural_factor(3.0)` returns approximately `1.0`.
   - `test_optimize_params()`: Feed exact data (e.g., generated with known $C$ and $k$) to `optimize_params` and assert it recovers the parameters within $10^{-4}$.

5. **Execution and Output**:
   In `analyze.py`, include a `__main__` block that reads `/home/user/observations.csv`, runs `optimize_params`, `solve_structural_factor` (using the optimized $C$), and `mcmc_sample`. 
   It must output a JSON file at `/home/user/results.json` with exactly these keys: `"opt_C"`, `"opt_k"`, `"factor_x"`, `"mcmc_C"`, `"mcmc_k"`.
   
   Create a bash script `/home/user/run_pipeline.sh` that:
   - Installs `numpy`, `scipy`, and `pytest` using pip.
   - Runs the test suite via `pytest /home/user/test_analyze.py`.
   - Executes `python /home/user/analyze.py`.

Ensure all files have the correct permissions and your bash script is executable.