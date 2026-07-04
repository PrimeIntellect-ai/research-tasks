You are acting as a data scientist trying to fit an ODE model to a set of noisy observations using Bayesian inference. Your previous attempts using a simple grid search were computationally intractable. You need to implement a parallelized Markov Chain Monte Carlo (MCMC) pipeline to estimate the parameters efficiently.

The system is a damped harmonic oscillator described by the following system of Ordinary Differential Equations (ODEs):
dy1/dt = y2
dy2/dt = -2 * gamma * y2 - omega^2 * y1

Where:
- `y1` is the position.
- `y2` is the velocity.
- `gamma` is the damping coefficient.
- `omega` is the angular frequency.

Initial conditions are fixed at `y1(0) = 1.0` and `y2(0) = 0.0`.
The observation data is located at `/home/user/oscillator_data.csv`, which contains two columns: `t` (time) and `y1_obs` (noisy observations of position). The measurement noise is known to be Gaussian with standard deviation `sigma = 0.1`.

Your task is to write and execute a Python script that performs the following:
1. Load the data from `/home/user/oscillator_data.csv`.
2. Define the ODE model and solve it using `scipy.integrate.solve_ivp` at the time points `t` provided in the CSV data. Use the `RK45` method.
3. Define the log-prior, log-likelihood, and log-posterior functions. Assume uniform priors for both parameters: `0 < gamma < 1` and `1 < omega < 5`. If parameters are outside this range, the log-prior should be `-np.inf`.
4. Use the `emcee` Python package to perform MCMC sampling. 
   - Use `32` walkers.
   - Run for `1000` steps.
   - Initialize the walkers by adding Gaussian noise (standard deviation = `0.01`) to the starting guess `gamma=0.2, omega=3.0`.
5. **Parallelism**: Utilize the `multiprocessing.Pool` within `emcee` with exactly 4 worker processes to speed up the likelihood evaluations.
6. **Reproducibility**: To ensure reproducible results, call `numpy.random.seed(42)` exactly before generating the initial walker positions and running the sampler.
7. Discard the first `500` steps as burn-in and flatten the remaining chain.
8. Calculate the mean of the posterior samples for `gamma` and `omega`.
9. Save the calculated means to a JSON file at `/home/user/posterior_mean.json` with the format:
   ```json
   {
       "gamma": 0.123,
       "omega": 3.456
   }
   ```
   (Round the values to 3 decimal places).

Note: You may need to install necessary packages like `emcee`, `scipy`, and `numpy` using pip. Ensure your script executes successfully and generates the requested JSON file.