You are an AI assistant helping a systems researcher organize and analyze simulated server telemetry data to predict server crashes. 

The raw data consists of three CSV files located in `/home/user/data/`: `server_1.csv`, `server_2.csv`, and `server_3.csv`. Each file contains the following columns: `cpu_usage`, `memory_usage`, `disk_io`, `network_in`, `network_out`, and the target variable `crash` (1 for crash, 0 for healthy).

Your task is to write and execute a Python script (`/home/user/process_and_train.py`) that performs the following end-to-end machine learning pipeline:

1. **Environment Setup**: Install any necessary Python libraries (e.g., `pandas`, `scikit-learn`).
2. **Data Ingestion**: Read and concatenate all three server CSV files into a single dataset.
3. **Feature Engineering**: Create a new feature called `cpu_mem_ratio`, calculated as `cpu_usage / memory_usage`.
4. **Sampling**: The dataset is highly imbalanced (crashes are rare). Separate your features (all columns except `crash`) and target (`crash`). Then, oversample the minority class (`crash == 1`) so that its count exactly matches the majority class (`crash == 0`). 
   * *Requirement*: Use `sklearn.utils.resample` to upsample the minority class. You must set `random_state=42` for the resampling process.
5. **Feature Selection**: Use `sklearn.feature_selection.SelectKBest` with the `f_classif` scoring function to select the top 3 features from your balanced dataset.
6. **Modeling and Tuning**: Train a `RandomForestClassifier(random_state=42)` using `GridSearchCV`. Use 3-fold cross-validation (`cv=3`).
   * *Hyperparameter Grid*: `{'max_depth': [3, 5, None], 'n_estimators': [10, 50]}`.
7. **Reporting**: Extract the best hyperparameters, the best cross-validation score, and the names of the 3 selected features. Write these results to a JSON file at `/home/user/results.json`.

The `/home/user/results.json` file must have exactly this format:
```json
{
  "selected_features": ["feature_1", "feature_2", "feature_3"],
  "best_max_depth": null,
  "best_n_estimators": 10,
  "best_cv_score": 0.9876
}
```
*Note: Sort the `selected_features` array alphabetically. Round the `best_cv_score` to exactly 4 decimal places.*

Ensure your script runs successfully and creates the final JSON file.