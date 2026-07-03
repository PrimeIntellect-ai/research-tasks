I am working on preparing training data for a system load prediction model, but my pipeline is failing due to some subtle data issues. I have a dataset located at `/home/user/data/sensor_log.csv`.

Please write and run a Python script to perform the following data processing and modeling tasks:

1. **Data Cleaning & Feature Engineering**: 
   Load the dataset. The `event_count` column represents integer counts, but some values are missing and represented as empty strings, which causes pandas to load the column as floats with NaNs. 
   - Impute the missing values in `event_count` using the median of the non-missing values in that column.
   - Cast the `event_count` column strictly back to an integer (`int`) data type.

2. **Correlation Analysis & Feature Selection**:
   - Compute the absolute Pearson correlation coefficient between `sensor_1` and all other feature columns (excluding the target column `system_load`).
   - Identify any features that have an absolute correlation strictly greater than `0.80` with `sensor_1`.
   - Drop those highly correlated features from the dataset to avoid multicollinearity (do NOT drop `sensor_1` itself, and do NOT drop `system_load`).

3. **Bayesian Modeling & Hyperparameter Tuning**:
   - Separate the dataset into features (`X`) and the target (`y = system_load`).
   - Use `sklearn.linear_model.BayesianRidge` to model the data.
   - Perform hyperparameter tuning using `sklearn.model_selection.GridSearchCV`.
   - Use standard 3-fold cross-validation (`cv=3`, no shuffling).
   - Search over the following grid for these exact four parameters: `alpha_1`, `alpha_2`, `lambda_1`, `lambda_2`. For each parameter, test the values `[1e-6, 1e-2]`.

4. **Model Validation**:
   - Retrieve the best estimator from the GridSearch.
   - Use this best estimator to predict `system_load` on the *entire* dataset.
   - Compute the Mean Squared Error (MSE) of these predictions.

5. **Reporting**:
   Save the final pipeline results to a JSON file at `/home/user/pipeline_results.json` with the following structure:
   ```json
   {
       "dropped_columns": ["list", "of", "dropped", "column", "names"],
       "best_params": {
           "alpha_1": 0.0,
           "alpha_2": 0.0,
           "lambda_1": 0.0,
           "lambda_2": 0.0
       },
       "mse": 0.0000
   }
   ```
   *Note: Ensure the `dropped_columns` list is sorted alphabetically. Round the `mse` to 4 decimal places.*