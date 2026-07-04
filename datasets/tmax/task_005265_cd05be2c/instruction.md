You are helping a data scientist debug a parameter estimation script. They are trying to fit a damped harmonic oscillator model to some observed noisy data using Markov Chain Monte Carlo (MCMC). 

The physics model is given by the ODE:
$m \frac{d^2x}{dt^2} + c \frac{dx}{dt} + k x = 0$
where mass $m = 1.0$, $c$ is the damping coefficient, and $k$ is the spring constant. The initial conditions are $x(0) = 1.0$ and $x'(0) = 0.0$.

The data is stored in an HDF5 file located at `/home/user/project/data.h5`. It contains two datasets:
- `/t`: Time points of the observations.
- `/y`: Noisy observations of the position $x$.

The provided script `/home/user/project/fit.py` implements a basic Metropolis-Hastings MCMC to estimate the posterior of $c$ and $k$. However, the script is currently failing. The MCMC either crashes with overflow warnings or rejects almost all proposals. The data scientist suspects that the naive numerical integrator used in the forward model is numerically unstable and diverging for the typical parameter ranges, ruining the likelihood calculations.

Your task is to:
1. Identify and fix the numerical instability in the `solve_ode` function inside `/home/user/project/fit.py`. You may replace the naive Euler integrator with a robust method from `scipy.integrate` (e.g., `solve_ivp` or `odeint`).
2. Ensure the script correctly reads the observation data from the HDF5 file.
3. Run the MCMC sampler for 5000 iterations.
4. Discard the first 1000 iterations as burn-in.
5. Compute the posterior mean of $c$ and $k$ from the remaining 4000 samples.
6. Save the results to `/home/user/project/results.txt` exactly in the following format (rounded to 2 decimal places):
```
c_mean: X.XX
k_mean: Y.YY
```

You can run the script and use the terminal as needed. Make sure you use robust numerical methods to prevent divergence.