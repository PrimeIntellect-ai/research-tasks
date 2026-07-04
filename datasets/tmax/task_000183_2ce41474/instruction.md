You are a Machine Learning Engineer preparing a synthetic dataset to train a surrogate neural network for epidemiological forecasting. To ensure the generated dataset is robust and statistically stable, you need to build a reproducible Python computation pipeline that simulates the SIR (Susceptible-Infected-Recovered) model under parameter uncertainty, and evaluates the expected maximum infection peak using Monte Carlo and bootstrap methods.

Write a Python script at `/home/user/generate_data.py` that does the following:

1. **ODE Simulation:** Implement the standard SIR model using `scipy.integrate.odeint`. 
   The equations are:
   - dS/dt = -beta * S * I / N
   - dI/dt = beta * S * I / N - gamma * I
   - dR/dt = gamma * I
   
   Initial conditions: N = 1000 (total population), I(0) = 10, R(0) = 0, S(0) = N - I(0) - R(0).
   Time span: t = 0 to 100, evaluated at 1000 evenly spaced points (using `numpy.linspace(0, 100, 1000)`).

2. **Monte Carlo Simulation:** 
   You must set the global random seed to exactly `42` using `numpy.random.seed(42)` at the very beginning of your execution logic.
   Run exactly M = 1000 simulations.
   For each simulation, sample `beta` from a uniform distribution U(0.2, 0.5) and `gamma` from a uniform distribution U(0.05, 0.15). Sample arrays of size 1000 for betas and gammas before the loop.
   For each simulation, solve the ODE and record the maximum number of infected individuals at any time step (`I_max`).

3. **Bootstrap Confidence Intervals:**
   After collecting the 1000 `I_max` values, calculate the sample mean of `I_max`.
   Then, use the bootstrap method to compute the 95% confidence interval for this mean.
   - Perform exactly 2000 bootstrap resamples.
   - For each resample, draw M=1000 items from your `I_max` array with replacement.
   - Calculate the mean of each resample.
   - Use `numpy.percentile` to find the 2.5th and 97.5th percentiles of the 2000 bootstrap means.

4. **Output Verification:**
   The script must save the final statistics to a JSON file located at `/home/user/sir_ml_data_stats.json`. 
   The JSON must have exactly these keys:
   - `"mean_I_max"`: The float value of the sample mean of `I_max`.
   - `"ci_lower_95"`: The float value of the 2.5th percentile.
   - `"ci_upper_95"`: The float value of the 97.5th percentile.

You will need to install any required Python packages (e.g., `scipy`, `numpy`) and then execute your script. Make sure the output JSON is formatted correctly and exists at the specified path before finishing.