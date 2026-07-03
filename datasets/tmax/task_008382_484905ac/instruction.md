You are a data engineer tasked with building an ETL script that processes messy sensor data, engineers features, trains a baseline model, and evaluates it using bootstrap resampling.

We have a raw dataset located at `/home/user/data/sensor_readings.csv`. It contains the following columns:
`timestamp`, `s1`, `s2`, `s3`, `s4`, `s5`, and `target`.

Write a Python script at `/home/user/etl_pipeline.py` that performs the following steps in this exact order:

1. **Missing Value Handling**: Load the CSV. The sensor columns (`s1` to `s5`) contain missing values (`NaN`). Impute these missing values using the median of each respective column.
2. **Outlier Handling**: After imputation, clip the values of `s1` to `s5` to their respective 5th and 95th percentiles (calculated after imputation). Values below the 5th percentile should be set to the 5th percentile, and values above the 95th percentile should be set to the 95th percentile.
3. **Feature Engineering**: Parse the `timestamp` column (format: `YYYY-MM-DD HH:MM:SS`) and create a new integer column called `hour` (0-23) representing the hour of the day. Drop the original `timestamp` column.
4. **Dimensionality Reduction**: Apply Principal Component Analysis (PCA) to the cleaned `s1` to `s5` columns to reduce them to exactly 2 components (`pca1` and `pca2`). Use `sklearn.decomposition.PCA` with `svd_solver='full'`. Drop the original `s1` to `s5` columns, keeping only `hour`, `pca1`, `pca2`, and `target`.
5. **Model Training**: Train a standard linear regression model (`sklearn.linear_model.LinearRegression`) using `hour`, `pca1`, and `pca2` as features to predict `target`. Train it on the entire dataset.
6. **Evaluation & Bootstrapping**: 
   - Calculate the Mean Squared Error (MSE) of the model's predictions on the entire dataset.
   - Set `numpy.random.seed(42)`.
   - Perform exactly 1,000 bootstrap resamples of the dataset to estimate the 95% confidence interval of the MSE. To do this:
     - In a loop of 1000 iterations, sample `N` indices with replacement (where `N` is the total number of rows).
     - Calculate the MSE for each bootstrap sample (using the actuals and the model's predictions for those sampled indices). Note: Do NOT retrain the model on the bootstrap samples; just evaluate the already-trained model on them.
   - Calculate the 2.5th and 97.5th percentiles of these 1,000 MSE values using `numpy.percentile`.

7. **Reporting**: Save the results as a JSON file at `/home/user/metrics.json` with the following structure:
```json
{
  "mse": <float>,
  "mse_ci_lower": <float>,
  "mse_ci_upper": <float>
}
```

Run your script to generate the `/home/user/metrics.json` file. Ensure the file is valid JSON and the values are accurate.