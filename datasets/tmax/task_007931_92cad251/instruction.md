You are a performance engineer working on profiling scientific computing applications. Your team relies heavily on MCMC sampling for parameter estimation in Ordinary Differential Equation (ODE) models. Before integrating a heavy probabilistic programming framework like PyMC or Stan, you need to write a lightweight, pure NumPy/SciPy baseline MCMC sampler to profile the raw computational overhead of the ODE solver.

You have been provided a reference dataset `/home/user/data.csv` containing noisy experimental observations of a radioactive decay process.

The system is modeled by the ODE:
dy/dt = -θ * y
With the initial condition: y(0) = 100.0.

Your task is to write a Python script `/home/user/mcmc_profiler.py` that implements a Random Walk Metropolis-Hastings MCMC sampler to estimate the posterior distribution of the decay rate parameter `θ` and calculate the acceptance rate as a rudimentary convergence/efficiency metric.

Specifications for your script:
1. **Data Loading**: Read `/home/user/data.csv`. The first column is time `t`, and the second is the observed value `y_obs`.
2. **ODE Solving**: Use `scipy.integrate.solve_ivp` to solve the ODE at the exact time points `t` found in the dataset.
3. **Statistical Model**:
    *   **Prior**: Uniform distribution U(0, 1). If a proposal is outside (0, 1), its log-prior probability is -infinity.
    *   **Likelihood**: The observations have independent Gaussian noise with a known standard deviation σ = 2.0. The log-likelihood should be calculated as `sum(-0.5 * ((y_obs - y_pred) / 2.0)**2)`. Ignore constant terms (like log(2π)) for the likelihood calculation.
4. **MCMC Algorithm**:
    *   Set the initial parameter value to `θ = 0.1`.
    *   Before the MCMC loop begins, initialize the random seed strictly using `np.random.seed(42)`.
    *   Run exactly 5000 iterations.
    *   **In each iteration, exactly in this order**:
        1. Draw a proposal: `theta_prop = np.random.normal(theta_current, 0.05)`
        2. Draw a uniform random number for the acceptance criterion: `u = np.random.rand()`
        3. Accept the proposal if `np.log(u) < (log_posterior(theta_prop) - log_posterior(theta_current))`.
5. **Output**:
    *   Discard the first 1000 samples as burn-in.
    *   Calculate the posterior mean of `θ` from the remaining 4000 samples.
    *   Calculate the overall acceptance rate (total accepted proposals / 5000).
    *   Save these two values to `/home/user/results.json` in the following exact format:
        `{"theta_mean": <float>, "acceptance_rate": <float>}`

Write and execute the script. Ensure `/home/user/results.json` is created with the correct values.