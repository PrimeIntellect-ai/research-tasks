You are a Machine Learning Engineer preparing a data processing pipeline for manufacturing sensor data. Your goal is to build a robust, reproducible ETL and modeling pipeline that utilizes dimensionality reduction, hyperparameter tuning, and statistical hypothesis testing to validate improvements.

Data files are located in `/home/user/data/`:
1. `/home/user/data/sensor_features.csv`: Contains `sample_id` and 20 noisy continuous sensor readings (`sensor_0` to `sensor_19`). Some values are missing.
2. `/home/user/data/sensor_targets.csv`: Contains `sample_id` and the continuous `target` variable.

Write a Python script at `/home/user/run_pipeline.py` that performs the following:

**1. ETL & Preprocessing:**
- Load and merge the features and targets on `sample_id`.
- Sort the data by `sample_id` ascending.
- Impute missing values in sensor columns using the mean of each column.
- Standardize the sensor features (zero mean, unit variance). Use `random_state=42` wherever applicable in your script.

**2. Dimensionality Reduction:**
- Fit Principal Component Analysis (PCA) on the scaled features.
- Determine the minimum number of principal components required to explain strictly greater than `90.0%` (> 0.90) of the total variance.

**3. Modeling & Tuning:**
- **Baseline Model:** Train a Ridge Regression model (`alpha=1.0`) on the original standardized features (not PCA). Evaluate using 5-fold cross-validation (shuffle=True, random_state=42). Record the Mean Squared Error (MSE) for each fold.
- **PCA Model:** Train a Ridge Regression model on the PCA-transformed features (using the number of components determined above). Tune the `alpha` parameter over the grid `[0.1, 1.0, 10.0, 100.0]` using GridSearchCV with 5-fold cross-validation (shuffle=True, random_state=42). Select the `alpha` that yields the best mean MSE. Record the MSE for each of the 5 folds for this best model.

**4. Statistical Hypothesis Testing:**
- Perform a two-sided paired t-test comparing the 5 fold MSEs of the Baseline Model against the 5 fold MSEs of the best PCA Model.
- Calculate the p-value.
- Calculate the 95% Confidence Interval (CI) of the difference in means (`baseline_MSE - pca_MSE`). Use the t-distribution with 4 degrees of freedom.

**5. Output:**
Your script must output a JSON file at `/home/user/results.json` containing exactly these keys:
- `"n_components"`: (integer) The number of PCA components chosen.
- `"best_alpha"`: (float) The best alpha from GridSearchCV.
- `"baseline_mean_mse"`: (float) Mean CV MSE for the baseline.
- `"pca_mean_mse"`: (float) Mean CV MSE for the tuned PCA model.
- `"p_value"`: (float) The p-value from the paired t-test.
- `"ci_lower"`: (float) Lower bound of the 95% CI of the MSE difference.
- `"ci_upper"`: (float) Upper bound of the 95% CI of the MSE difference.

Ensure your code is perfectly reproducible. Running `python3 /home/user/run_pipeline.py` multiple times should yield the exact same `results.json`.