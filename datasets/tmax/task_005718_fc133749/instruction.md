You are a data engineer building a lightweight ETL and modeling pipeline. We are testing a new model in a resource-constrained container, so we need to strictly control numerical library threading while tracking our experiments.

You have two datasets in your home directory:
1. `/home/user/users.csv` (Columns: `user_id`, `age`, `signup_days`)
2. `/home/user/transactions.csv` (Columns: `user_id`, `total_spend`, `txn_count`)

Write and execute a Python script at `/home/user/pipeline.py` that performs the following steps:
1. **Configure Numerical Libraries**: Before importing pandas, numpy, or scikit-learn, set the environment variables `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` to `"1"` inside the script using `os.environ` to ensure single-threaded execution.
2. **Multi-source Data Joining**: Read both CSV files and perform an inner join on `user_id`.
3. **Cross-validation and Hyperparameter Tuning**: 
   - Extract features `X` (`age`, `signup_days`, `txn_count`) and target `y` (`total_spend`).
   - Use `sklearn.linear_model.Ridge` as your estimator.
   - Use `sklearn.model_selection.GridSearchCV` with 3-fold cross-validation (`cv=3`).
   - Tune the `alpha` hyperparameter testing the values: `[0.1, 1.0, 10.0]`.
4. **Experiment Tracking**: Fit the GridSearchCV on the joined data. Then, extract the `best_params_['alpha']` and the `best_score_`. 
   - Write these to a JSON file at `/home/user/experiment_results.json` with exactly this format:
     ```json
     {
       "best_alpha": 10.0,
       "best_score": 0.12345
     }
     ```
     *(Note: 10.0 and 0.12345 are just examples, your script should write the actual evaluated values).*

Ensure you run your script so the `/home/user/experiment_results.json` file is successfully generated before concluding.