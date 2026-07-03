You are tasked with building a robust data processing and model training pipeline. We have a dataset at `/home/user/dataset.csv` containing user data, but it has some data quality issues that cause standard pandas pipelines to silently convert integer columns to floats due to missing values.

Write a Python script at `/home/user/pipeline.py` that performs the following steps:
1. Loads the CSV file `/home/user/dataset.csv`. The file has three columns: `feature_A`, `feature_B`, and `label`.
2. The `feature_A` column represents integer counts, but it contains some missing values represented by the string `"MISSING"`. 
3. Calculate the median of the valid values in `feature_A`. Replace all `"MISSING"` values with this median. Convert the imputed median to an integer (using standard rounding/floor) before imputing, so no floats are introduced.
4. Ensure that after imputation, the `feature_A` column is strictly of pandas type `int64`.
5. Train a `RandomForestClassifier` from `scikit-learn` using `feature_A` and `feature_B` as predictors for `label`. You must initialize the model with `random_state=42` and all other parameters as default.
6. Calculate the accuracy of the model on the training data.
7. Benchmark inference performance: time how long it takes to run `model.predict(X)` on the training features `X`, repeated 100 times in a simple loop.
8. Save the results to a JSON file at `/home/user/results.json` with the exact following keys:
   - `"median_A"`: The integer median value used for imputation.
   - `"feature_A_dtype"`: The string representation of the pandas dtype of `feature_A` after your cleaning step (should be `"int64"`).
   - `"accuracy"`: The training accuracy (a float).
   - `"inference_time_sec"`: The total time in seconds taken for the 100 prediction iterations (a float).

Run your script to produce the `/home/user/results.json` file. You may install any necessary Python packages (like pandas, scikit-learn) using pip.