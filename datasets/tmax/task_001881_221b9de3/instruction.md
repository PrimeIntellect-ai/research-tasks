You are a Data Scientist tasked with building a robust data cleaning and evaluation pipeline. 

We have three datasets located in `/home/user/data/`:
1. `users.csv`: Contains `user_id` (int), and `age` (int).
2. `transactions.csv`: Contains `user_id` (int), `store_id` (int), and `amount` (float). Note that not all users have transactions.
3. `labels.csv`: Contains `user_id` (int) and `churned` (int, 0 or 1).

Your goal is to write a Python script at `/home/user/pipeline.py` that performs the following steps:

**Phase 1: Multi-source Joining & Feature Engineering**
1. Read the three CSV files.
2. Perform a left join of `transactions` and `labels` onto the `users` dataframe using `user_id`.
3. **Data Integrity Fix**: When pandas performs a left join, missing transactions introduce `NaN` values, which silently converts integer columns like `store_id` into floats. This breaks our downstream categorical handlers. 
   - You must fill missing `store_id` values with `-1` and explicitly convert the `store_id` column back to standard `int64`.
   - Fill missing `amount` values with `0.0`.
   - Assume all users have labels (no missing `churned` values).

**Phase 2: Model Training**
1. Define your feature matrix `X` using columns `['age', 'store_id', 'amount']` and target `y` using `['churned']`.
2. Split the data into training and testing sets using `train_test_split` with `test_size=0.2` and `random_state=42`.
3. Train a `RandomForestClassifier` with `random_state=42` on the training data.
4. Calculate the standard accuracy on the test set.

**Phase 3: Bootstrap Evaluation**
1. To understand the variance of our model, perform bootstrap sampling on the **test set** to compute a 95% Confidence Interval for the accuracy.
2. Set `numpy.random.seed(42)`.
3. For 1000 iterations:
   - Resample the test set indices with replacement (sample size equal to the test set size).
   - Compute the accuracy of the model's predictions on this resampled test set.
4. Calculate the 2.5th and 97.5th percentiles of these 1000 accuracy values using `numpy.percentile`.

**Phase 4: Output**
Your script must output a JSON file to `/home/user/pipeline_results.json` with the following structure:
```json
{
  "store_id_dtype": "int64",
  "base_accuracy": <float>,
  "ci_lower": <float>,
  "ci_upper": <float>
}
```

You are allowed to install necessary packages (like `pandas` and `scikit-learn`) using pip. 
Run your script to produce the output JSON file.