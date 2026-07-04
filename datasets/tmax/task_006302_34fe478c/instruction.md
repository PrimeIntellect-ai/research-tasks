You are a data engineer building an analytical ETL pipeline for IoT manufacturing sensors. You have been given a raw dataset at `/home/user/sensor_data.csv` that contains messy sensor readings (`sensor_A`, `sensor_B`) and a `target` variable representing machine efficiency. 

Your goal is to build a pipeline script (in any language you choose, though Python with pandas and scikit-learn is recommended) that performs data cleaning, feature engineering, and baseline model training.

Please perform the following steps exactly as specified:
1. **Missing Value Handling**: Column `sensor_A` contains missing values (NaNs). Impute these missing values using linear interpolation. If any NaNs remain at the edges, fill them using a forward-fill followed by a backward-fill.
2. **Outlier Handling**: Column `sensor_B` contains extreme anomalies. Clip the values in `sensor_B` to its 5th and 95th percentiles (inclusive).
3. **Feature Engineering**: 
   - Create a new column `A_B_ratio` defined as the imputed `sensor_A` divided by the clipped `sensor_B`.
   - Create a new column `rolling_mean_A` which is the rolling mean of the imputed `sensor_A` with a window size of 3. Use a minimum period of 1 (so the first row is just its own value, the second row is the mean of the first two, etc.).
4. **Regression**: Train a standard Linear Regression model (without any regularization) to predict the `target` column using four features: `sensor_A` (imputed), `sensor_B` (clipped), `A_B_ratio`, and `rolling_mean_A`. Train it on the entire dataset.

Finally, calculate the Mean Squared Error (MSE) of your model's predictions on the same dataset. 

Write the final results to `/home/user/pipeline_results.json`. The JSON file must have exactly this structure:
```json
{
  "imputed_A_sum": <float, sum of sensor_A after imputation>,
  "clipped_B_mean": <float, mean of sensor_B after clipping>,
  "mse": <float, mean squared error of the linear regression model>
}
```
Round all float values in the JSON to exactly 4 decimal places.