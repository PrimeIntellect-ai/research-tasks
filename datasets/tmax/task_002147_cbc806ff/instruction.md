You are a machine learning engineer tasked with preparing and selecting features for a server failure prediction model. 

You have been provided with a raw dataset located at `/home/user/server_metrics.csv`. This dataset contains the following columns: `timestamp`, `cpu_usage`, `mem_usage`, `disk_io`, `net_rx`, `net_tx`, and `status` (where 0 indicates normal operation and 1 indicates a failure).

Your task is to write and execute a Python script that performs the following data preparation pipeline:

1. **ETL & Feature Engineering:**
   - Load the CSV file.
   - Drop any rows containing missing (`NaN` or empty) values.
   - Create two new engineered features: 
     - `cpu_mem_ratio`: The ratio of `cpu_usage` to `mem_usage` (i.e., `cpu_usage / mem_usage`).
     - `total_net`: The sum of `net_rx` and `net_tx`.

2. **Correlation Analysis & Feature Selection:**
   - Calculate the Pearson correlation coefficient between all numerical features (`cpu_usage`, `mem_usage`, `disk_io`, `net_rx`, `net_tx`, `cpu_mem_ratio`, `total_net`) and the target variable `status`.
   - Identify the top 3 features that have the highest *absolute* correlation with `status`.

3. **Hypothesis Testing:**
   - For these top 3 selected features, perform an independent two-sample Welch's t-test (assuming unequal variances) to compare the feature's distribution when `status == 0` versus `status == 1`.

4. **Reporting:**
   - Save the results for the top 3 features to a JSON file located precisely at `/home/user/selected_features.json`.
   - The JSON should be a dictionary where the keys are the feature names, and the values are dictionaries containing the keys `"correlation"` and `"p_value"`. Round both numbers to 4 decimal places.
   
Example expected output format for `/home/user/selected_features.json`:
```json
{
  "total_net": {
    "correlation": 0.8521,
    "p_value": 0.0001
  },
  "cpu_usage": {
    "correlation": -0.7123,
    "p_value": 0.0034
  },
  "cpu_mem_ratio": {
    "correlation": 0.6432,
    "p_value": 0.0123
  }
}
```

Write the script, execute it, and ensure the JSON file is created successfully.