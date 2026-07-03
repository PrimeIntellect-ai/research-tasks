You are acting as a data scientist fitting a dynamical model to experimental data. 
You have been given a workspace at `/home/user/model_fitting` with several files, but the pipeline is currently broken.

Your goals are to fix the numerical integrator, complete the MCMC sampling script to estimate model parameters, ensure the regression tests pass, and visualize the results.

Here is the context and what you need to do:

1. **Fix the Integrator (`integrator.py`)**:
   The file `integrator.py` contains a custom adaptive Runge-Kutta 4 (RK4) ODE solver. It is currently diverging or taking extremely small steps because the step-size adaptation logic is incorrect. 
   Find the bug in the step-size update rule and fix it. The correct formula for updating the step size `h` based on the error `err` and tolerance `tol` should be:
   `h_new = 0.9 * h * (tol / max(err, 1e-15))**0.2`
   Ensure the solver correctly integrates from `t0` to `tf`.

2. **Regression Testing (`test_integrator.py`)**:
   Run `pytest /home/user/model_fitting/test_integrator.py`. You must fix `integrator.py` until this test passes. The test checks your integrator against `scipy.integrate.solve_ivp` for a simple harmonic oscillator.

3. **Complete the MCMC Sampler (`mcmc.py`)**:
   The file `mcmc.py` is incomplete. You need to implement a Metropolis-Hastings MCMC sampler to fit the parameters `[omega, gamma]` of a damped harmonic oscillator to the data provided in `data.csv`.
   - The proposal distribution should be a multivariate normal. To draw proposals, use the Cholesky decomposition of the provided covariance matrix `cov_matrix` (do not use `np.random.multivariate_normal` directly; compute the Cholesky factor `L` and use `L @ z` where `z` is standard normal).
   - The log-likelihood function should assume Gaussian noise with standard deviation `sigma = 0.5`.
   - Run the MCMC sampler for 5000 iterations.
   - Save the accepted samples as a numpy array in `/home/user/model_fitting/posterior_samples.npy`.
   - Calculate the mean of the posterior samples (discarding the first 1000 as burn-in) and save it as a JSON file at `/home/user/model_fitting/map_estimate.json` with keys `"omega"` and `"gamma"`.

4. **Visualization (`plot_fit.py`)**:
   Write a script `/home/user/model_fitting/plot_fit.py` that:
   - Loads `data.csv`, `posterior_samples.npy`, and `map_estimate.json`.
   - Simulates the model using the estimated mean parameters.
   - Plots the experimental data as scatter points and the fitted model as a solid line.
   - Saves the plot to `/home/user/model_fitting/fit_plot.png`.

Run the full pipeline so that all requested output files are generated.