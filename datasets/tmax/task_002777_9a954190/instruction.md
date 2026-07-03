I am an ML engineer preparing training data to train a Neural ODE on the dynamics of a Van der Pol (VDP) oscillator. To generate the dataset of parameters, I am using an MCMC method to sample the oscillator's stiffness parameter `mu` from a posterior distribution. 

I have written a script located at `/home/user/vdp_mcmc.py`. However, my custom numerical integrator inside `simulate_vdp` diverges for stiff parameters (e.g., when `mu > 1.0`) because it uses a naive fixed-step Euler method. Because of this wrong step-size adaptation, the trajectories blow up, the log-likelihood evaluates to `-inf`, and the MCMC sampler rejects almost all proposals.

Your task is to fix the integrator, run the MCMC sampling, and perform density estimation on the results.

Please complete the following steps:

1. **Scientific Environment Management**:
   - Create a Python 3 virtual environment at `/home/user/venv`.
   - Activate it and install `numpy`, `scipy`, `emcee`, and `scikit-learn`.

2. **Fix the Numerical Integrator (Convergence Testing)**:
   - Edit `/home/user/vdp_mcmc.py`.
   - Replace the buggy `simulate_vdp(mu)` function. Use `scipy.integrate.solve_ivp` to integrate the system from `t=0` to `t=10` with initial conditions `y = [2.0, 0.0]`. 
   - To ensure convergence for stiff parameters, you **must** use `method='BDF'` and set `t_eval=[10.0]`. 
   - The function should return the value of `y[0]` at `t=10.0`. If the integration fails (i.e., `res.success` is False), return `None`.
   - Do not change the random seed or MCMC parameters already present in the script.

3. **MCMC Sampling**:
   - Run the updated `/home/user/vdp_mcmc.py` using your virtual environment. It will produce a file named `/home/user/valid_mu_samples.npy` containing the flattened 1D array of valid MCMC samples.

4. **Density Estimation**:
   - Write a new script, `/home/user/fit_density.py`, that loads `/home/user/valid_mu_samples.npy`.
   - Reshape the samples to a 2D array of shape `(-1, 1)` and fit a 1D Kernel Density Estimator (KDE) using `sklearn.neighbors.KernelDensity`. Use a `gaussian` kernel and a bandwidth of `0.5`.
   - Evaluate the log-density (using the `score_samples` method) of the fitted KDE at the following test points for `mu`: `[1.0, 2.0, 3.0, 4.0, 5.0]`.
   - Save the resulting 5 log-density values as a standard JSON list of floats to `/home/user/kde_results.json`.

Make sure all output files are exactly where specified.