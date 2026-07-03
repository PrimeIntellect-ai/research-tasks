You are an AI assistant helping a data scientist debug and automate a model-fitting pipeline.

We are fitting a simple ordinary differential equation (ODE) model of radioactive decay ($dx/dt = -\theta x$) to experimental data found in `/home/user/data.csv`. We estimate the parameter $\theta$ using a Metropolis-Hastings MCMC algorithm implemented in `/home/user/mcmc_ode.py`. 

However, the MCMC chain is currently diverging or producing nonsensical results. The root cause is that the custom Euler numerical integrator inside the likelihood function uses an inappropriately large step size.

Your task is to:
1. Fix the numerical integrator in `/home/user/mcmc_ode.py` by decreasing the step size `dt` to `0.1`. Do not change the random seed or other MCMC parameters.
2. Run the MCMC script. It will generate a file named `trace.csv` containing the samples of $\theta$.
3. Write a new script `/home/user/analyze.py` (or `.R`) that:
   - Reads `trace.csv`.
   - Discards the first 500 rows as burn-in.
   - Calculates the mean of the remaining $\theta$ samples.
   - Saves this mean value to `/home/user/posterior_mean.txt`, rounded to 3 decimal places.
   - Generates a trace plot (a line plot of the $\theta$ samples after burn-in) and saves it as `/home/user/trace_plot.png`.
4. Create a reproducible bash script `/home/user/pipeline.sh` that executes the fixed `mcmc_ode.py` followed by your `analyze` script. Ensure `pipeline.sh` is executable.

The final state must include `/home/user/posterior_mean.txt`, `/home/user/trace_plot.png`, and `/home/user/pipeline.sh`.