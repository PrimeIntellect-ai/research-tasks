You are a performance engineer tasked with profiling a mathematical sampling pipeline. We need a reproducible pipeline that performs optimization, runs a Markov Chain Monte Carlo (MCMC) sampler, and profiles the execution to identify bottlenecks.

Create a Python script at `/home/user/sampler.py` and a `Makefile` at `/home/user/Makefile` to automate the pipeline.

**Mathematical Problem:**
We are analyzing the 2D Rosenbrock function: $f(x, y) = (1 - x)^2 + 100(y - x^2)^2$.
The target distribution for our sampler is $P(x,y) \propto \exp(-f(x,y) / 10.0)$.

**Pipeline Requirements:**
1. **Reproducibility:** In `/home/user/sampler.py`, set the numpy random seed to `42` at the very beginning of the execution. Use `numpy.random` for all random operations.
2. **Optimization:** Start at an initial guess of `[0.0, 0.0]`. Use `scipy.optimize.minimize` (with the `BFGS` method) to find the minimum of the Rosenbrock function. Write the optimized coordinates `x` and `y` to `/home/user/opt_result.txt` formatted to 4 decimal places, separated by a space (e.g., `1.0000 1.0000`).
3. **MCMC Sampling:** Implement a Metropolis-Hastings sampler.
    *   Start the chain exactly at the optimized coordinates found in step 2.
    *   Use a Gaussian proposal distribution with a standard deviation of $\sigma=0.5$ for both dimensions.
    *   Run the chain for exactly `100,000` iterations.
    *   Acceptance probability: $\min(1, \exp(-(f(prop) - f(curr)) / 10.0))$.
4. **Profiling:** Profile *only* the execution of your MCMC sampling function using `cProfile`. 
    *   Save the binary profile data to `/home/user/mcmc_profile.prof`.
    *   Calculate the mean of the 100,000 samples across both dimensions and save it to `/home/user/mcmc_mean.txt` (same format as `opt_result.txt`, 4 decimal places).
    *   Use the `pstats` module within the script to read the profile data, sort by `tottime`, and output the top 10 lines to `/home/user/profile_stats.txt`.
5. **Makefile:** Create a `/home/user/Makefile` with a target `all` that:
    *   Ensures `scipy` and `numpy` are installed (e.g., via `pip`).
    *   Executes `python3 /home/user/sampler.py`.

Run your pipeline by executing `make all` before considering the task complete.