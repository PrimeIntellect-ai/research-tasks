You are an AI assistant acting as a data scientist. Your task is to fit a non-linear decay model to an experimental dataset and estimate the uncertainty of the decay rate using bootstrap resampling.

We have a dataset located at `/home/user/data.npz` which contains two 1D NumPy arrays: `t` (time) and `y` (measured signal).

The underlying physical model for the signal is expected to be an exponential decay:
`y(t) = alpha * exp(-beta * t)`

Your task:
1. Write a Python script `/home/user/analyze_decay.py` that performs the following steps.
2. Load the dataset from `/home/user/data.npz`.
3. Use `scipy.optimize.curve_fit` to find the optimal parameters `alpha` and `beta`. Use initial guesses `alpha=1.0` and `beta=1.0`.
4. Perform non-parametric bootstrapping to estimate the 95% confidence interval for the `beta` parameter.
   - Resample the data points `(t_i, y_i)` as pairs with replacement.
   - Perform exactly 2000 bootstrap iterations.
   - Before starting the bootstrap loop, set the random seed exactly via `numpy.random.seed(42)` to ensure reproducibility.
   - For each bootstrap sample, fit the model using `curve_fit` (again with initial guesses `1.0` and `1.0`). If a fit fails to converge, skip that sample and do not include it in the final statistics.
5. Calculate the 2.5th and 97.5th percentiles of the successfully fitted `beta` values to form the 95% confidence interval.
6. Save the results to a JSON file at `/home/user/results.json` with the following format:
```json
{
  "beta_opt": <float, the optimal beta from the original data>,
  "beta_lower": <float, 2.5th percentile from bootstrap>,
  "beta_upper": <float, 97.5th percentile from bootstrap>
}
```
7. Execute the script so that `results.json` is generated. You may install `numpy` and `scipy` using pip if they are not already installed.