You are an AI assistant acting as a data analyst. I have two CSV datasets located at `/home/user/data/users.csv` and `/home/user/data/transactions.csv`. 

The `users.csv` file has columns: `user_id,age,income`.
The `transactions.csv` file has columns: `user_id,spend`.

Your task is to write a bash script `/home/user/analyze.sh` that performs the following pipeline:

1. **Multi-source data joining**: Use Bash utilities (like `sort`, `join`, `awk`, etc.) to inner-join the two datasets on `user_id`. Ensure the output has exactly one header row: `user_id,age,income,spend`. Save the joined dataset to `/home/user/joined.csv`. (Do not use Python or Pandas for this step; strictly use Bash/GNU utilities).
2. **Sampling and bootstrap**: Using Bash tools, generate 3 independent bootstrap samples (sampling *with replacement*) of the data rows from `joined.csv`. Each sample should have the same number of data rows as `joined.csv` and must include the header row. Save them as `/home/user/sample_1.csv`, `/home/user/sample_2.csv`, and `/home/user/sample_3.csv`.
3. **Cross-validation and hyperparameter tuning**: For each generated sample, write and execute an inline Python script (using `scikit-learn`) that reads the sample CSV, uses `age` and `income` as features (X) and `spend` as the target (y). Perform a Grid Search with 3-fold cross-validation to find the best `alpha` hyperparameter for a `Ridge` regression model. Test the following `alpha` values: `[0.1, 1.0, 10.0]`. 
4. **Output reporting**: The bash script must append the best `alpha` for each sample to a log file at `/home/user/best_alphas.txt` in exactly this format:
```
Sample 1: 1.0
Sample 2: 0.1
Sample 3: 10.0
```

Requirements:
- The script `/home/user/analyze.sh` must be executable and run without errors.
- Ensure all intermediate files are generated in `/home/user/`.
- Use a random seed of `42` in your Python script's cross-validation (e.g., in KFold or if using any random state) to ensure determinism, but note that the bash bootstrap sampling might be non-deterministic depending on how you use `shuf`.