You are a Machine Learning Engineer responsible for preparing training data and building a robust predictive model for a manufacturing plant. You have been provided with a dataset of sensor readings and operational efficiency targets at `/home/user/sensor_data.csv`.

The dataset contains five sensor features (`sensor_1` through `sensor_5`) and a continuous target variable (`efficiency`). The data is noisy: it contains missing values and extreme outliers that represent sensor glitches.

Your task is to write and execute a Python script that builds an end-to-end Machine Learning pipeline. The script must perform the following precise steps to ensure reproducibility:

1. **Data Splitting**: Read `/home/user/sensor_data.csv`. Separate the features and target. Split the data into a training set (80%) and a testing set (20%) using `sklearn.model_selection.train_test_split` with `random_state=42`.

2. **Missing Value Handling**: `sensor_1` and `sensor_2` contain missing values (NaN). Calculate the median for these features **using only the training set**. Fill the missing values in both the training and testing sets with these respective medians.

3. **Outlier Handling**: `sensor_3` contains extreme high-value outliers. Compute the 1st percentile and the 99th percentile of `sensor_3` **using only the training set**. Clip (limit) the values of `sensor_3` in both the training and testing sets so that any value below the 1st percentile is set to the 1st percentile, and any value above the 99th percentile is set to the 99th percentile.

4. **Model Training & Hyperparameter Tuning**: 
   - Use a `RandomForestRegressor` with `random_state=42`.
   - Perform hyperparameter tuning using `sklearn.model_selection.GridSearchCV` with 5-fold cross-validation (`cv=5`).
   - Use the following parameter grid:
     - `n_estimators`: [50, 100, 200]
     - `max_depth`: [5, 10, None]
   - Fit the GridSearchCV on your processed training data.

5. **Evaluation & Reporting**: 
   - Predict the `efficiency` on your processed testing data using the best estimator found by GridSearchCV.
   - Calculate the Root Mean Squared Error (RMSE) on the test set.
   - Save the results to a JSON file strictly located at `/home/user/pipeline_results.json`.
   
The JSON file must have exactly this structure and key naming (round `test_rmse` to exactly 4 decimal places):
```json
{
  "best_max_depth": <int or null>,
  "best_n_estimators": <int>,
  "test_rmse": <float>
}
```

Ensure you install any necessary libraries (e.g., `pandas`, `scikit-learn`, `numpy`) if they are missing. Leave the JSON file exactly at `/home/user/pipeline_results.json` when you are done.