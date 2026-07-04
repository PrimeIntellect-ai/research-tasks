You are a Data Engineer building an automated quality check for an ETL pipeline. 

You have been provided with incoming sensor tabular data at `/home/user/data/raw_metrics.csv`. 
You also have the weights of a previously trained Anomaly Scoring model in `/home/user/data/model_weights.json`.

Your task is to:
1. Reconstruct the anomaly scoring model and run inference on the tabular data. The model is a simple linear transformation: `Score = (f1 * W1) + (f2 * W2) + (f3 * W3) + b`. The weights and bias are in the JSON file.
2. Transform and aggregate the data: Create a new column called `is_anomaly`. If the `Score` is strictly greater than `0.5`, the row is an anomaly (`1`); otherwise, it is normal (`0`).
3. Group the data by `is_anomaly`. For each group (normal and anomaly), calculate the Pearson correlation coefficient between features `f4` and `f5`.
4. Output your results to exactly `/home/user/output/analysis.json`. Ensure the directory exists.

The output JSON file must follow this exact schema:
```json
{
  "correlation_normal": 0.12345,
  "correlation_anomaly": -0.54321
}
```
Round the correlation values to 5 decimal places. If a correlation cannot be calculated (e.g., standard deviation is zero or group is empty), set its value to `null`.