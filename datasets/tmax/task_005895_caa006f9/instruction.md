You are a Machine Learning Engineer preparing training data for a surrogate model of a thermal system. The true underlying system follows a simple cooling Ordinary Differential Equation (ODE). 

You have been provided with two files in your home directory (`/home/user/`):
1. `reference_data.csv`: A dataset containing noisy observations of time and temperature.
2. `mcmc_ode.py`: A Python module containing a function `run_mcmc(seed)`. This function reads the reference data, runs a Markov Chain Monte Carlo (MCMC) algorithm to sample the posterior distribution of the cooling rate parameter $k$, and returns the mean of the posterior after burn-in.

Currently, running multiple MCMC chains sequentially is too slow for your pipeline. Your task is to parallelize this process using Python.

Instructions:
1. Write a Python script named `/home/user/parallel_mcmc.py`.
2. In your script, import `run_mcmc` from `mcmc_ode.py`.
3. Use Python's built-in `multiprocessing.Pool` to run `run_mcmc(seed)` concurrently for the following four random seeds: `[42, 43, 44, 45]`.
4. Calculate the average of the 4 returned $k$ estimates.
5. Write the final averaged $k$ value to `/home/user/final_k.txt`. The value must be formatted to exactly four decimal places (e.g., `0.1452`).
6. Run your script so that `/home/user/final_k.txt` is successfully generated.