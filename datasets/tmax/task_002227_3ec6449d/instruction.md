You are a performance engineer tasked with profiling a scientific application that models population dynamics. A recent update to the simulation engine requires a formal regression test and uncertainty quantification.

Your goal is to write a Python script at `/home/user/profile_regression.py` that performs an ODE regression test against a baseline and computes bootstrap confidence intervals for the simulation's outputs under perturbed parameters.

### Part 1: Regression Testing (ODE Solving)
We model a predator-prey system using the Lotka-Volterra equations:
dx/dt = alpha*x - beta*x*y
dy/dt = delta*x*y - gamma*y

Standard parameters: `alpha=1.5`, `beta=1.0`, `delta=1.0`, `gamma=3.0`.
Initial conditions: `x(0) = 10.0`, `y(0) = 5.0`.
Time span: `t = 0` to `t = 10`.

1. Solve this ODE using `scipy.integrate.solve_ivp`. Use the default `RK45` solver, and evaluate the solution at exactly 200 evenly spaced time points between 0 and 10 (inclusive).
2. Read the baseline data from `/home/user/baseline.csv` (which contains a header `t,x,y`).
3. Compute the maximum absolute error for the `x` variable between your simulation and the baseline data.

### Part 2: Uncertainty Profiling (Bootstrap Confidence Intervals)
Next, you must profile how sensitive the maximum prey population is to variations in the `alpha` parameter.
1. Run the ODE solver 200 times. For each run `i` (where `i` goes from 0 to 199), set `alpha = 1.5 + 0.1 * np.sin(i)`. Keep all other parameters and settings the same as Part 1.
2. For each run, record the maximum value of the prey population `x` over the simulated time points. You should end up with an array of 200 maximum values.
3. Compute the 95% bootstrap confidence interval for the **mean** of these maximum values.
   - Use exactly 1000 bootstrap resamples.
   - Each resample should draw 200 items with replacement from your collected array.
   - Use `numpy.random.seed(42)` immediately before your resampling loop/function for reproducibility.
   - Use `numpy.percentile` to find the 2.5th and 97.5th percentiles of the bootstrapped means.

### Output Specification
Your script must output a JSON file to `/home/user/report.json` with the following exact keys:
* `"max_abs_error_x"`: The maximum absolute error calculated in Part 1 (float).
* `"ci_lower"`: The 2.5th percentile of the bootstrapped means (float).
* `"ci_upper"`: The 97.5th percentile of the bootstrapped means (float).

The baseline file `/home/user/baseline.csv` has already been generated and placed on the system. You just need to create and execute `/home/user/profile_regression.py`.