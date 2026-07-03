You are an AI assistant helping an astrophysics researcher analyze simulated exoplanet transit data. 

The researcher has generated a dataset of lightcurves stored in an HDF5 file located at `/home/user/data/lightcurves.h5`. 
The file contains two datasets:
- `time`: A 1D array of shape `(1000,)` representing time in days.
- `flux`: A 2D array of shape `(100, 1000)` representing normalized flux measurements for 100 different simulated stars.

Your task is to build a reproducible Python pipeline to extract the parameters of a specific transit using Markov Chain Monte Carlo (MCMC).

Please do the following:
1. Isolate the lightcurve at index `41` (the 42nd lightcurve) from the `flux` dataset.
2. We assume the transit dip can be modeled by an inverted Gaussian: 
   `f(t) = 1.0 - A * exp(-0.5 * ((t - t0) / sigma)^2)`
3. Write a Python script that uses the `emcee` package to estimate the parameters `A` (depth), `t0` (transit center), and `sigma` (width) for this specific lightcurve.
4. Use the following MCMC configuration:
   - **Log-likelihood:** Assume Gaussian errors on the flux with a known standard deviation of `0.005`.
   - **Priors:** Uniform priors where `A` is in `[0.0, 1.0]`, `t0` is in `[0.0, 10.0]`, and `sigma` is in `[0.01, 2.0]`. If outside this range, log-prior is `-inf`.
   - **Walkers:** 32 walkers.
   - **Initialization:** Initialize the 32 walkers by adding Gaussian noise with standard deviation `1e-4` to the initial guess `[0.1, 5.0, 0.5]` (for `A`, `t0`, `sigma` respectively).
   - **Steps:** Run for `1000` steps.
   - **Random Seed:** Set the numpy random seed to `42` right before initializing your walkers and running the sampler for reproducibility.
5. Discard the first `200` steps as burn-in, and flatten the chain.
6. Calculate the mean of the posterior distribution for each parameter.
7. Save the resulting mean parameters to a JSON file at `/home/user/results/params.json` with the following format:
   `{"A": <float>, "t0": <float>, "sigma": <float>}`

You may need to install necessary Python packages like `h5py`, `numpy`, and `emcee`. The output directory `/home/user/results` might need to be created if it does not exist.