You are a Data Scientist tasked with cleaning and processing a messy sensor dataset using a combination of shell commands and scripting (Python or R). 

Your tasks are to set up the environment, perform statistical data cleaning, and build a robust imputation model.

Setup:
1. Create a virtual Python environment at `/home/user/venv` and activate it (or install necessary packages in your user space if using R).
2. The raw data is located at `/home/user/data/sensors_raw.csv`.

Data Cleaning and Analysis Pipeline:
1. **Correlation Analysis**: Identify if any two sensors have a Pearson correlation coefficient greater than `0.95`. Drop the sensor that appears *later* in the column order (e.g., if `sensor_X` and `sensor_Y` are highly correlated and `sensor_Y` is after `sensor_X`, drop `sensor_Y`).
2. **Bootstrap Estimation**: `sensor_D` contains noisy but valuable data. Use a bootstrap method (10,000 resamples, random seed 42) to estimate the mean of `sensor_D`.
3. **Cross-validation and Imputation**: The column `target_temp` contains missing values (NaN). Build a Ridge Regression model to predict `target_temp` using the remaining valid sensor columns (do not use `sensor_D` for this model, only use the remaining cleaned sensors). 
   - Use 5-fold cross-validation to select the best L2 penalty (`alpha` or `lambda`) from this exact grid: `[0.1, 1.0, 10.0]`. 
   - Set the random state/seed to 42 where applicable.
   - Use the best model to impute the missing values in `target_temp`.

Output Verification:
Create a JSON report at `/home/user/report.json` with the following exact keys:
- `"dropped_column"`: (string) The name of the highly correlated column you dropped.
- `"bootstrap_mean_sensor_D"`: (float) The bootstrap estimated mean of `sensor_D` (rounded to 2 decimal places).
- `"best_ridge_alpha"`: (float) The chosen hyperparameter from the CV process.

Save the final cleaned and imputed dataset to `/home/user/cleaned_sensors.csv`. It should contain the original columns minus the dropped one, with all missing values in `target_temp` replaced by your model's predictions. Keep the original row order.