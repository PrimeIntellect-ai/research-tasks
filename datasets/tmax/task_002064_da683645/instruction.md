You are a data scientist fitting an ODE model to time-series observations. 

I have a Jupyter Notebook at `/home/user/mcmc_fit.ipynb` that loads data from an HDF5 file (`/home/user/observations.h5`) and runs a simple Metropolis-Hastings MCMC algorithm to estimate the posterior distribution of two parameters (`alpha` and `beta`). 

However, the notebook currently fails to execute. The likelihood function uses a custom explicit Euler integrator to solve the ODE, but the step size (`dt = 0.5`) is too large, causing the numerical integrator to diverge and throw an overflow/NaN error during the MCMC steps.

Your task is to:
1. Fix the step-size adaptation issue in the notebook by changing the hardcoded integrator step size from `dt = 0.5` to `dt = 0.01`.
2. Execute the notebook headlessly (e.g., using `jupyter nbconvert` or similar tools). The notebook is already programmed to write the resulting MCMC samples to a new HDF5 file at `/home/user/posterior.h5` containing a dataset named `chain`.
3. Read the generated `/home/user/posterior.h5` file, compute the mean of the posterior samples for the `alpha` parameter (the first column of the `chain` dataset, ignoring the first 100 burn-in samples), and save this mean value to `/home/user/alpha_mean.txt` rounded to exactly 2 decimal places.

Ensure you do not alter the random seeds or the number of MCMC steps in the notebook, so the output remains deterministic.