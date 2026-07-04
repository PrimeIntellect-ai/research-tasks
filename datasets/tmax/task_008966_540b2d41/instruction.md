You are a Data Engineer debugging an ETL pipeline and running an analysis. 

The system currently has the following files in `/home/user/`:
- `transactions.csv`: Contains `tx_id`, `user_id`, `amount`, and `test_group` (A or B).
- `user_metadata.csv`: Contains `user_id` and `age_score` (an integer metric).
- `etl.py`: A buggy script that merges these datasets. 
- `anomaly_model.pkl`: A scikit-learn `IsolationForest` model.

**Your Tasks:**

1. **Environment Setup:** Create a Python virtual environment in `/home/user/venv` and install `pandas`, `scikit-learn`, and `scipy`. All subsequent Python scripts should be run using this environment.

2. **Fix the ETL Pipeline:** 
   The current `etl.py` performs a left join of transactions with user_metadata. Because some `user_id`s in `transactions.csv` are missing from `user_metadata.csv`, pandas silently converts the `age_score` column to `float` and introduces NaNs.
   Update or replace `etl.py` to:
   - Perform the left join.
   - Impute missing `age_score` values using the **median** `age_score` of the *available* valid rows in the merged dataset.
   - Cast the `age_score` column strictly back to an integer type.
   - Save the cleaned dataset to `/home/user/processed_data.csv` (keep the columns `tx_id`, `user_id`, `amount`, `test_group`, `age_score`).

3. **Model Inference:**
   Write a script to load `/home/user/processed_data.csv` and `/home/user/anomaly_model.pkl`. 
   - The model expects features: `['amount', 'age_score']` (in that exact order).
   - Use the model's `predict()` method to identify anomalies. (Note: Scikit-learn's IsolationForest returns `-1` for anomalies and `1` for normal instances).
   - Use the model's `decision_function()` method to compute raw anomaly scores.

4. **Hypothesis Testing:**
   Using the raw anomaly scores (from `decision_function()`), perform an independent two-sample t-test (assuming equal variances) to compare the anomaly scores of users in `test_group == 'A'` versus `test_group == 'B'`.

5. **Reporting:**
   Generate a final report file at `/home/user/results.json` with exactly the following JSON structure:
   ```json
   {
       "imputed_median": 0,          // The integer median value you used to fill NaNs
       "num_anomalies": 0,           // Total number of anomalies (where predict == -1)
       "t_statistic": 0.0000,        // T-statistic comparing Group A and Group B scores (rounded to 4 decimal places)
       "p_value": 0.0000             // P-value of the t-test (rounded to 4 decimal places)
   }
   ```