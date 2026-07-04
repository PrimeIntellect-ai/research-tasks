You are a Data Engineer tasked with building an end-to-end ETL and modeling pipeline to process raw manufacturing sensor data. 

You have been provided with two input files:
1. `/home/user/sensor_readings.csv` - Contains `timestamp` and 5 sensor readings (`sensor_A`, `sensor_B`, `sensor_C`, `sensor_D`, `sensor_E`).
2. `/home/user/target_values.csv` - Contains `timestamp` and `target_value` (a continuous variable we want to predict).

Your objective is to write and execute a Python script that performs the following steps in order:

**1. Data Transformation and Merging:**
- Read both CSV files and merge them on the `timestamp` column (inner join).
- Sort the merged data chronologically by `timestamp`.

**2. Feature Engineering:**
- Create rolling mean features for `sensor_A` and `sensor_B`. The rolling window should be exactly 3 steps, and you must use a minimum period of 1 (so the first row is just its own value, the second is the mean of the first two). Name these new columns `sensor_A_roll3` and `sensor_B_roll3`.
- Drop any rows containing NaN values after merging (if any exist).

**3. Correlation Analysis & Selection:**
- Compute the Pearson correlation matrix for all features (the original 5 sensors + the 2 new rolling features). Exclude `timestamp` and `target_value` from this analysis.
- Find pairs of features that have an absolute correlation strictly greater than `0.85`.
- For any such pair, drop the feature that comes *last* alphabetically. (e.g., if `sensor_A` and `sensor_A_roll3` are highly correlated, drop `sensor_A_roll3`). 
- Keep a list of the final selected feature names.

**4. Numerical Library Configuration & Modeling:**
- Configure NumPy to raise an error on division by zero using `np.seterr(divide='raise')`.
- Set up a Ridge regression model from `scikit-learn`.
- Use `GridSearchCV` to perform 5-fold cross-validation to find the best `alpha` hyperparameter. Test the following alpha values exactly: `[0.1, 1.0, 10.0, 100.0]`. 
- Use negative mean squared error (`neg_mean_squared_error`) as the scoring metric. Set `random_state=42` if the cross-validator requires it, and shuffle=False (standard TimeSeries/KFold without shuffle). *Actually, just use standard `KFold(n_splits=5, shuffle=False)`*.

**5. Reporting:**
Save the results of your pipeline to a JSON file located at `/home/user/pipeline_results.json`. The JSON file must have exactly this structure:
```json
{
  "selected_features": ["list", "of", "strings", "alphabetical_order"],
  "best_alpha": 1.0,
  "best_cv_mse": 0.12345
}
```
*Note: `best_cv_mse` should be the positive Mean Squared Error of the best model (multiply the negative MSE by -1), rounded to 5 decimal places.*

Write the Python script, run it, and ensure the JSON file is generated successfully.