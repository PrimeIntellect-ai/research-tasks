You are an MLOps engineer tasked with analyzing experiment artifacts to track and recommend the best model configurations. You have historical run metadata, but it contains messy logs that need cleaning. After cleaning, you must train a surrogate model to predict model accuracy based on hyperparameters and deployment latency, and then use it to recommend the best configuration for a new edge device.

Your workspace is located at `/home/user/mlops/`. Two files are provided:
1. `runs.csv` - Historical experiments with columns: `run_id`, `learning_rate`, `batch_size`, `latency_ms`, `accuracy`.
2. `candidates.csv` - New configurations being considered with columns: `run_id`, `learning_rate`, `batch_size`, `latency_ms`.

Please perform the following steps using Python:

**1. Data Cleaning:**
Read `runs.csv`. 
* Outlier Handling: Remove any rows where `latency_ms` is less than 0 or greater than 1000.
* Missing Values: After removing outliers, some rows may have an empty (NaN) `accuracy`. Fill these missing `accuracy` values with the exact mean of the `accuracy` values from the remaining valid rows.

**2. Model Training & Hyperparameter Tuning:**
Train a surrogate model to predict `accuracy` using `learning_rate`, `batch_size`, and `latency_ms` as features.
* Use `sklearn.ensemble.RandomForestRegressor` with `random_state=42`.
* Use `sklearn.model_selection.GridSearchCV` to perform 3-fold cross-validation (`cv=3`).
* Search over the hyperparameter grid: `max_depth` in `[2, 5, 10]`.
* Use `scoring='neg_mean_squared_error'`.
* Train the grid search on the entirely cleaned `runs.csv` dataset. 

**3. Inference and Recommendation:**
Read `candidates.csv`. 
* Use your best trained model to predict the `accuracy` for all candidate runs.
* Filter the candidates to only include those that meet strict edge deployment constraints: `latency_ms <= 50`.
* Out of the filtered candidates, find the one with the highest predicted `accuracy`.

**4. Reporting:**
Create a JSON report at `/home/user/mlops/report.json` containing the findings. The JSON must exactly match this format:
```json
{
  "best_max_depth": <integer>,
  "recommended_run_id": "<string>",
  "predicted_accuracy": <float>
}
```
*Note: Ensure all paths used are absolute. The system has scikit-learn and pandas installed.*