You are a data scientist tasked with benchmarking numerical models against highly oscillatory signals. Your goal is to compute the definite integral of the function `f(x) = sin(100 * x) * exp(-x)` from `x = 0` to `x = 5`.

A junior colleague attempted this using standard numerical integrators, but the integrator diverged or returned inaccurate results due to poor step-size adaptation on the highly oscillatory function. You need to fix the baseline integration, perform a Monte Carlo convergence test, and visualize the results.

Please perform the following steps:
1. Create a Python virtual environment at `/home/user/scipy_env` and install `numpy`, `scipy`, and `matplotlib`.
2. Write a Python script `/home/user/run_experiment.py` that does the following:
   - Defines the function `f(x) = sin(100 * x) * exp(-x)`.
   - Computes the "true" integral over `[0, 5]` using `scipy.integrate.quad`. To avoid step-size divergence issues, ensure you pass the argument `limit=1000` to `quad`.
   - Writes the resulting integral value (just the numerical float, rounded to 6 decimal places) to `/home/user/quad_result.txt`.
   - Performs a Monte Carlo integration of the same function over the interval `[0, 5]` using uniform sampling. Use sample sizes `N = [10000, 50000, 100000, 500000]`. 
   - Before generating any random numbers for the Monte Carlo integration, set the random seed exactly once using `numpy.random.seed(42)`.
   - Saves the Monte Carlo results to a CSV file at `/home/user/mc_convergence.csv`. The file must have the exact header `N,Estimate,Error`, where `Error` is the absolute difference between the Monte Carlo estimate and the "true" integral computed by `quad`.
   - Generates a log-log plot of `Error` (y-axis) vs `N` (x-axis) and saves the figure to `/home/user/convergence.png`.
3. Execute the script using the python interpreter from the virtual environment you created.