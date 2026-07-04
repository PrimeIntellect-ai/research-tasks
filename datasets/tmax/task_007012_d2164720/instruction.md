You are a data engineer tasked with building an end-to-end ETL and modeling pipeline. We have two datasets located in `/home/user/data/`:
1. `users.csv` (Columns: `user_id`, `age`, `account_balance`, `credit_score`)
2. `transactions.csv` (Columns: `transaction_id`, `user_id`, `amount`, `is_fraud`)

Your goal is to write a Python script `/home/user/pipeline.py` that performs the following steps:
1. **Multi-source joining:** Read both CSV files and perform an inner join on `user_id`.
2. **Preprocessing:** Drop the `user_id` and `transaction_id` columns. Impute any missing values in the remaining feature columns (`age`, `account_balance`, `credit_score`, `amount`) with the mean of that column.
3. **Dimensionality Reduction:** Apply Principal Component Analysis (PCA) to reduce the feature space (the 4 feature columns) down to exactly 3 principal components. Set `random_state=42` for PCA if applicable, though standard PCA is deterministic.
4. **Model Training & Cross-Validation:** Using the 3 principal components as your features $X$ and `is_fraud` as your target $y$, train a `RandomForestClassifier` (with `random_state=42`). Perform Grid Search with 3-fold cross-validation (`cv=3`) to tune the `max_depth` hyperparameter. Test the values: `[3, 5, 7]`.
5. **Experiment Tracking:** Extract the best `max_depth` and its corresponding mean cross-validation accuracy. Save these metrics to a JSON file at `/home/user/experiment_log.json` with the exact following structure:

```json
{
    "best_max_depth": 5,
    "best_cv_accuracy": 0.8523
}
```
*Note: The accuracy should be a float rounded to exactly 4 decimal places.*

You may need to install standard data science libraries (like `pandas` and `scikit-learn`) to complete this task. You can use standard pip commands to install them. Run your script to produce the output JSON file.