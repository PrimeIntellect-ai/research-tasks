You are acting as a data scientist fitting a nonlinear model to noisy experimental data. 

You have a dataset located at `/home/user/data.csv` containing two columns: `x` and `y`.
The data is believed to follow a model implicitly defined by the equation:
`y + sin(a * y) = b * x`
where `a` and `b` are unknown parameters.

Your objective is to estimate the parameters `a` and `b`, and quantify their uncertainties using a Monte Carlo simulation. 

Please write and execute a Python script `/home/user/fit_model.py` that performs the following steps:
1. Load the data from `/home/user/data.csv`.
2. Define a function to solve the implicit nonlinear equation for `y_hat` given `x`, `a`, and `b`. You must use a nonlinear equation solver (e.g., `scipy.optimize.fsolve` or `root`) to find `y_hat`. Use `b * x` as the initial guess for the solver.
3. Define an objective function that computes the Sum of Squared Errors (SSE) between the observed `y` and the predicted `y_hat`.
4. Find the best-fit parameters `(a_0, b_0)` by minimizing the SSE on the original data. Use an initial guess of `a = 0.5` and `b = 1.0`.
5. Perform a Monte Carlo simulation to estimate parameter uncertainties:
   - Run exactly `N = 100` iterations.
   - Set the random seed by calling `numpy.random.seed(42)` exactly ONCE before starting the loop.
   - In each iteration, generate a synthetic `y` array by adding Gaussian noise to the **original observed `y`**. The noise must be drawn using `numpy.random.normal(0, 0.1, len(y))`.
   - Fit the model to this synthetic `y` dataset to find `(a_k, b_k)`. Use the initial best-fit parameters `(a_0, b_0)` as the starting guess for the optimization of each synthetic dataset.
6. Compute the mean and standard deviation (using Delta Degrees of Freedom, ddof=1) of the 100 fitted `a_k` and `b_k` values.
7. Save the results to `/home/user/results.json` with the following structure:
```json
{
    "a_0": float,
    "b_0": float,
    "a_mean": float,
    "b_mean": float,
    "a_std": float,
    "b_std": float
}
```
Round all float values in the JSON to 4 decimal places.

Make sure to install any required packages (like `scipy`, `numpy`, `pandas`) using pip. Ensure your numerical solvers are stable and converge properly.