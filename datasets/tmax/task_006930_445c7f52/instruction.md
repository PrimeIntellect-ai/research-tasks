You are a Machine Learning Engineer preparing training data based on physical simulations. You have been given a script `/home/user/lorenz_ensemble.py` that solves an ensemble of Lorenz oscillators to generate dataset features. 

However, you've noticed that running the script multiple times produces `training_data.csv` files with the same values but in a non-deterministic order, making row-by-row regression testing and version control impossible. This is due to a floating-point/concurrency reduction order issue in the script.

Your objectives:
1. **Fix the non-determinism**: Modify `/home/user/lorenz_ensemble.py` so that the output `training_data.csv` is perfectly deterministic across multiple runs. Do not change the random seed or the initial states, just the concurrency order.
2. **Generate Data**: Run the fixed script to generate `/home/user/training_data.csv`.
3. **Statistical Regression Test**: Write a script `/home/user/test_regression.py` that performs a 2-sample Kolmogorov-Smirnov (KS) test between the `z` column of your new `training_data.csv` and a provided `/home/user/reference_data.csv`. This ensures your concurrency fix didn't alter the underlying statistical distribution of the simulation.
4. **Output Report**: Your script `/home/user/test_regression.py` must execute the KS test and output a JSON file at `/home/user/regression_report.json` with the following structure:
```json
{
  "ks_statistic": 0.0,
  "p_value": 1.0,
  "is_deterministic": true,
  "reference_mean_z": 24.5
}
```
- `ks_statistic` and `p_value`: The results of `scipy.stats.ks_2samp` between the two `z` columns.
- `is_deterministic`: A boolean (set to `true` if your fix ensures identical CSV outputs on consecutive runs).
- `reference_mean_z`: The float mean of the `z` column from `/home/user/reference_data.csv`.

Ensure your output JSON strictly matches these keys.