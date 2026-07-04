You are a data engineer building a reproducible ETL and modeling pipeline. We have a raw dataset located at `/home/user/raw_data.csv` which contains noisy data.

Your task is to write a Python script at `/home/user/pipeline.py` that performs the following steps when executed:

1. **Data Schema Enforcement:**
   - Load `/home/user/raw_data.csv`.
   - Keep only the columns: `feature_A`, `feature_B`, and `target`. Ignore any other columns.
   - Drop any rows that have missing (NaN/null) values in any of these three columns.
   - Enforce data types: `feature_A` and `feature_B` must be floats. `target` must be a float. (If a row cannot be converted to a float, drop it. For simplicity, assume all remaining data can be safely cast).

2. **Cross-Validation and Hyperparameter Tuning:**
   - Using the cleaned data, set up a machine learning pipeline to predict `target` using `feature_A` and `feature_B`.
   - Use `sklearn.linear_model.Ridge`.
   - Perform a grid search using `sklearn.model_selection.GridSearchCV` with 3-fold cross-validation (`cv=3`).
   - Test the following values for the `alpha` hyperparameter: `[0.1, 1.0, 10.0]`.
   - Set `random_state=42` if your scaler or model requires it (Ridge solver='auto' is fine, random_state is not strictly needed for basic Ridge, but good practice). Set `scoring='neg_mean_squared_error'`.

3. **Output:**
   - The script must write the best `alpha` value found by GridSearchCV to a plain text file at `/home/user/best_alpha.txt`. The file should contain only the numerical value (e.g., `1.0`).

Execute your script to ensure `/home/user/best_alpha.txt` is created successfully.