You are a data analyst tasked with processing server metrics from CSV files to build a reproducible machine learning pipeline, tune hyperparameters, and ensure numerical accuracy through automated testing.

The raw data is located at `/home/user/data/metrics.csv`. It contains the following columns: `cpu_load`, `temperature`, `fan_speed`, and `power_consumption` (target). Some values in `fan_speed` are missing.

Perform the following steps:

1. **Environment Setup**: 
   Create a Python virtual environment at `/home/user/venv` and install `pandas`, `scikit-learn`, and `pytest`. Ensure you use this environment for all subsequent Python tasks.

2. **Pipeline Construction & Feature Engineering**:
   Write a Python script at `/home/user/pipeline.py` that loads the dataset and constructs a reproducible `scikit-learn` pipeline. 
   The pipeline must include a custom feature engineering step (or `ColumnTransformer`/`FunctionTransformer`) that:
   - Creates a new feature called `load_temp_ratio` calculated as `cpu_load / temperature`.
   - Imputes missing values in `fan_speed` using the median strategy.
   - Passes all features (including the original `cpu_load`, `temperature`, and imputed `fan_speed`, plus the new `load_temp_ratio`) to a `Ridge` regression model.

3. **Cross-Validation and Tuning**:
   In the same script, use `GridSearchCV` to perform 5-fold cross-validation to find the optimal `alpha` parameter for the Ridge model. 
   Evaluate `alpha` values of `[0.1, 1.0, 10.0]`. 
   Use Negative Mean Absolute Error (`neg_mean_absolute_error`) as the scoring metric. 
   Calculate the positive Mean Absolute Error (MAE) of the best model during cross-validation.

4. **Output Generation**:
   The script `/home/user/pipeline.py` must save a file named `/home/user/results.json` containing exactly the following keys:
   - `"best_alpha"`: The optimal alpha value found (float).
   - `"cv_mae"`: The best positive MAE score from the cross-validation (float).
   - `"median_fan_speed"`: The median fan speed calculated and used for imputation (float).

5. **Numerical Accuracy Testing**:
   Write a `pytest` test script at `/home/user/test_pipeline.py`. It should:
   - Import your pipeline/data logic.
   - Contain a test `test_mae_threshold` that asserts the pipeline's cross-validated MAE is strictly less than `15.0`.
   - Contain a test `test_no_missing_values` that asserts the feature transformer successfully removes/imputes all NaNs before hitting the estimator.
   
   Run the tests using your virtual environment's `pytest` and pipe the output to `/home/user/test_report.log` (e.g., `/home/user/venv/bin/pytest /home/user/test_pipeline.py > /home/user/test_report.log`).

When you are finished, the files `/home/user/pipeline.py`, `/home/user/test_pipeline.py`, `/home/user/results.json`, and `/home/user/test_report.log` must exist.