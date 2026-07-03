You are an MLOps engineer tasked with building a robust model evaluation pipeline to track experiment artifacts. We have collected a dataset of server metrics, but it is messy. You need to write a Python script that cleans the data, tunes a model using cross-validation, and estimates the confidence interval of the model's performance using bootstrap sampling.

Here are the specific requirements:

**1. Data Preparation:**
* The dataset is located at `/home/user/data/server_metrics.csv`. It contains features: `cpu_load`, `memory_usage`, `network_io`, and a target variable: `response_time`.
* **Missing Values:** The `memory_usage` column contains missing values (NaNs). Impute these missing values using the *median* of the `memory_usage` column.
* **Outliers:** The `response_time` column contains extreme outliers due to measurement errors. Remove any rows where `response_time` is strictly greater than the 99th percentile of the `response_time` column. 
* Do the imputation first, then the outlier removal.

**2. Data Splitting:**
* Split the cleaned dataset into a training set (80%) and a testing set (20%) using `scikit-learn`'s `train_test_split`.
* Use `random_state=42` for the split.

**3. Model Training and Hyperparameter Tuning:**
* Use a `RandomForestRegressor` with `random_state=42`.
* Perform hyperparameter tuning using `GridSearchCV` with 3-fold cross-validation (`cv=3`).
* Search the following parameter grid:
  * `n_estimators`: [10, 50, 100]
  * `max_depth`: [3, 5, None]
* Train the grid search on the training set to find the best model.

**4. Bootstrap Sampling for Confidence Intervals:**
* Using the best model from the grid search, make predictions on the **test set**.
* Perform bootstrap sampling to estimate the 95% confidence interval for the Mean Squared Error (MSE).
* **Bootstrap procedure:** Draw 1000 bootstrap samples (with replacement) from the paired (true target, predicted target) arrays of the test set. For each sample, compute the MSE. Use `random_state=42` for the random number generator used to create the bootstrap indices (e.g., `np.random.default_rng(42)`).
* Calculate the 2.5th and 97.5th percentiles of these 1000 MSE values to get the lower and upper bounds of the 95% confidence interval.

**5. Artifact Tracking (Output):**
* Save the experiment results to a JSON file located at `/home/user/artifacts/experiment_summary.json`.
* The JSON must have exactly this structure (with your computed values):
```json
{
  "best_params": {
    "max_depth": <value>,
    "n_estimators": <value>
  },
  "test_mse_ci_lower": <float>,
  "test_mse_ci_upper": <float>
}
```

Ensure you install any necessary dependencies (like `pandas`, `scikit-learn`, `numpy`) locally if they are not present. Create the `/home/user/artifacts` directory if it does not exist.