I am an ML engineer preparing training data from a simulation, but I've noticed that multi-threaded floating-point reductions are causing non-reproducible discrepancies in the aggregated features. I have compiled a dataset of these errors in `/home/user/discrepancies.csv`, which contains two columns: `N` (the number of elements aggregated) and `error` (the absolute difference from the exact sum).

I need you to perform a statistical and optimization analysis to characterize these errors. Please do the following:

1. Create a Python virtual environment at `/home/user/venv` and install the necessary scientific libraries (`numpy`, `scipy`, `pandas`, `matplotlib`).
2. Read the `/home/user/discrepancies.csv` dataset.
3. Compute a 95% bootstrap confidence interval for the mean of the `error` column. Use `scipy.stats.bootstrap` with the statistic as `np.mean`, `method='percentile'`, `n_resamples=10000`, and `random_state=42`.
4. We hypothesize the error scales according to the function `error_bound(N) = a * N^b`. Use `scipy.optimize.minimize` with the `Nelder-Mead` method to find the parameters `a` and `b` that minimize the Mean Squared Error (MSE) between the actual `error` and the predicted `error_bound`. Use an initial guess of `a = 1e-16` and `b = 1.0`.
5. Generate a scatter plot of the raw data (`N` vs `error`) overlaid with the fitted curve. Save this visualization as `/home/user/fit_plot.png`.
6. Save the results of your analysis to `/home/user/results.json` in the following format:
```json
{
  "bootstrap_ci_lower": <float>,
  "bootstrap_ci_upper": <float>,
  "optimized_a": <float>,
  "optimized_b": <float>
}
```

Ensure all files are saved in the correct locations and have the exact specified names.