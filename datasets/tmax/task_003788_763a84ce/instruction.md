I am a researcher trying to estimate the parameters of a damped harmonic oscillator model from noisy experimental data using MCMC, but my script keeps crashing and is too slow.

The model is defined by the ODE system:
dy1/dt = y2
dy2/dt = -k*y1 - c*y2

I have a dataset in an HDF5 file located at `/home/user/data.h5` containing two datasets: `t` (time points) and `y` (noisy observations of y1).

I wrote a Python script at `/home/user/fit_model.py` using `emcee` to sample the posterior distributions of `k` and `c`. However, it has two major issues:
1. **Divergence / Crashing**: The MCMC walkers randomly explore the parameter space, and sometimes propose negative values for `k` or `c`. This causes the ODE integrator to diverge, yielding `NaN` values, which crashes the `emcee` sampler. You need to fix the `log_prior` function so that it strictly enforces `k > 0` and `c > 0` (returning `-np.inf` for invalid values), preventing the ODE solver from even running for unphysical parameters.
2. **Performance**: The script runs on a single core. Please modify the `emcee.EnsembleSampler` instantiation in the script to use a `multiprocessing.Pool` with exactly 4 processes to run the walkers in parallel.

Once you have fixed the script:
1. Run it. The script is configured to use 32 walkers and 2000 steps. 
2. Discard the first 500 steps as burn-in.
3. Calculate the median (50th percentile) of the marginalized posterior for `k` and `c` from the flattened chain.
4. Save these median estimates to a JSON file at `/home/user/map_estimates.json` with the exact keys `"k"` and `"c"` (e.g., `{"k": 5.01, "c": 0.49}`).

You may need to install missing Python packages like `emcee`, `h5py`, and `scipy`.