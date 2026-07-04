You are an expert data scientist. You have been provided with some experimental decay data in `/home/user/decay_data.csv`. The data contains two columns: `time` and `y`.

The system is theorized to follow a non-linear decay process modeled by the following Ordinary Differential Equation (ODE):
dy/dt = -k * y - c * y^2
with the initial condition y(0) = 10.0.

Your objective is to find the parameters `k` and `c`, estimate their 95% confidence intervals using residual bootstrapping, and visualize the result.

Write and execute a Python script to perform the following steps:
1. Load the data from `/home/user/decay_data.csv`.
2. Use a numerical ODE solver (e.g., `scipy.integrate.odeint` or `solve_ivp`) to compute y(t) during the fitting process.
3. Find the best-fit parameters for `k` and `c` using non-linear least squares (minimizing the sum of squared residuals between the numerical ODE solution and the observed data). Use `[0.1, 0.1]` as the initial guess for `[k, c]`.
4. Perform residual bootstrapping with 200 iterations to find the 95% confidence intervals for `k` and `c`. 
   - Compute the residuals of the best fit.
   - Set the random seed with `np.random.seed(123)` immediately before starting your bootstrap loop.
   - For each of the 200 iterations, sample the residuals with replacement, add them to the best-fit model predictions to form new synthetic `y` values, and refit `k` and `c`. Use the initial best-fit parameters as the starting guess (`p0`) for the bootstrap fits.
5. Compute the 2.5th and 97.5th percentiles of the bootstrapped parameter distributions to form the 95% confidence intervals.
6. Save the confidence intervals to a text file at `/home/user/ci.txt` in the exact following format, with numbers rounded to 3 decimal places:
k: [lower, upper]
c: [lower, upper]
7. Generate a plot saved to `/home/user/fit_plot.png` that shows the original data as points and the best-fit model as a solid line.