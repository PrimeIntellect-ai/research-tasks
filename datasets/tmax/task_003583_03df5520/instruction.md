You are an AI assistant helping a data science researcher organize and statistically evaluate a dataset. The researcher has split their data into two CSV files located in your home directory:
1. `/home/user/features.csv` - Contains columns `sample_id`, `f1`, `f2`, `f3`.
2. `/home/user/targets.csv` - Contains columns `sample_id`, `target`.

Your task is to write and execute a Python script that does the following:

1. **Multi-source data joining**: Join `features.csv` and `targets.csv` on `sample_id`.
2. **Hyperparameter tuning & Cross-validation**: 
   - Define a Ridge Regression model (`sklearn.linear_model.Ridge`).
   - Find the optimal `alpha` penalty parameter from the choices `[0.1, 1.0, 10.0]` by minimizing the 5-fold cross-validated Mean Squared Error (MSE).
   - Use `sklearn.model_selection.KFold` with `n_splits=5`, `shuffle=True`, and `random_state=42` to evaluate each alpha. Use `cross_val_score` with `scoring='neg_mean_squared_error'` and negate the result to get MSE.
3. **Bootstrap method**: 
   - Using the *best* `alpha` found in the previous step, perform 100 bootstrap iterations to estimate the confidence bounds of the cross-validated MSE.
   - For each iteration `i` from 0 to 99 (inclusive), use `sklearn.utils.resample(joined_dataframe, random_state=i)` to create a bootstrapped sample of the joined dataset.
   - Calculate the 5-fold CV MSE of the bootstrapped sample (again using Ridge with the best alpha, and `KFold(n_splits=5, shuffle=True, random_state=42)`).
   - Store these 100 MSE scores.
4. **Reporting**:
   - Calculate the 5th and 95th percentiles of the 100 MSE scores using `numpy.percentile`.
   - Create a file `/home/user/bootstrap_results.txt` with exactly the following format:

```text
Best Alpha: <alpha_value>
5th Percentile: <value_rounded_to_4_decimals>
95th Percentile: <value_rounded_to_4_decimals>
```

Example of expected output format:
```text
Best Alpha: 1.0
5th Percentile: 0.1234
95th Percentile: 0.5678
```

Ensure the Python script runs successfully and creates the requested file.