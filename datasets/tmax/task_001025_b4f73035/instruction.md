I am a bioinformatics analyst working on modeling the mutation load of a viral sequence over time. I have written a Python script located at `/home/user/mcmc_mutations.py` which attempts to use Markov Chain Monte Carlo (MCMC) to fit a dynamic ODE model to my experimental data located in `/home/user/sequence_data.csv`.

Currently, I'm facing two major issues:
1. **Divergent Integrator:** The script uses a custom, fixed-step Euler method to integrate the ODE within the log-likelihood function. Whenever the MCMC proposes slightly larger parameter values, the integrator diverges (producing NaNs or infs), which ruins the MCMC acceptance rate. You need to replace the custom `solve_ode_euler` function with a robust adaptive step-size solver from SciPy (specifically, use `scipy.integrate.solve_ivp` with the `RK45` method).
2. **Lack of Parallelism:** The MCMC sampling is running sequentially and is very slow. Please modify the script to utilize parallel computing. Specifically, use Python's `multiprocessing.Pool` with 4 worker processes and pass it to the `emcee.EnsembleSampler`.

**Requirements:**
- Fix the ODE solver to use `scipy.integrate.solve_ivp(..., method='RK45')`.
- Parallelize the `emcee` sampler using `multiprocessing.Pool(processes=4)`.
- The script should run 50 walkers for 500 steps (discarding the first 100 steps as burn-in).
- After running the MCMC, calculate the mean of the posterior distribution for each of the three parameters ($r$, $K$, $d$).
- The script must save these posterior means into a JSON file at `/home/user/posterior_summary.json`. The file should have exactly this format:
```json
{
  "r_mean": 0.000,
  "K_mean": 0.000,
  "d_mean": 0.000
}
```
*(Replace `0.000` with the actual float values rounded to 3 decimal places).*

Please fix the script and run it to produce the correct `/home/user/posterior_summary.json` file.