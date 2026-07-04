You are a data analyst monitoring server health. You have received a dataset of system metrics and a set of weights for a logistic regression model trained to predict server failures. You need to write a Python script to process this data, reconstruct the model, run inference, and output the alerts.

Your task:
1. Read the input dataset at `/home/user/system_metrics.csv`.
2. Perform feature engineering to create a new feature called `cpu_mem_ratio`, calculated as `cpu_util` divided by `mem_util`. If `mem_util` is 0, set `cpu_mem_ratio` to 0.
3. Read the model parameters from `/home/user/model_weights.json`.
4. Reconstruct the logistic regression model using the formula: `P(failure) = 1 / (1 + e^-(w * X + b))`. 
   The features used by the model, in order, are: `cpu_util`, `disk_io`, and `cpu_mem_ratio`. The weights and bias are provided in the JSON file.
5. Run inference on the dataset to calculate the failure probability for each row.
6. Filter the results to include only rows where the failure probability is strictly greater than 0.8.
7. Save these filtered results to `/home/user/alerts.csv`. The output CSV must contain exactly two columns: `timestamp` and `probability`. The `probability` values must be rounded to exactly 4 decimal places.

Ensure your final output is properly formatted and saved to the exact path specified. You may install and use standard data science libraries like `pandas` and `numpy` if needed.