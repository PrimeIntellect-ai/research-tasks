You are a data analyst troubleshooting a data processing pipeline. The pipeline produces CSV files, but there are concerns about its reproducibility and numerical stability across different runs.

You have been provided with the outputs of two identical pipeline runs:
- `/home/user/run1_output.csv`
- `/home/user/run2_output.csv`

Your task is to write a Python script named `/home/user/evaluate_reproducibility.py` that analyzes these two files and generates an automated testing report. 

The script must perform the following steps:
1. Load both CSV files. You can assume they have the exact same structure, index, and column names.
2. Calculate the element-wise difference between the numeric columns of the two datasets (`difference = run1 - run2`).
3. Compute the maximum absolute difference across all numeric values to test numerical accuracy.
4. Assess reproducibility: the pipeline is considered reproducible if the maximum absolute difference is strictly less than `1e-5`.
5. To understand the nature of the numerical instability, calculate the covariance matrix of the `difference` dataframe. 
6. Identify the pair of distinct columns that have the highest absolute covariance in their differences. This indicates which features share correlated noise.

Finally, your script must output the results to a JSON file at `/home/user/test_report.json` with the exact following schema:
```json
{
  "max_abs_diff": <float>,
  "is_reproducible": <boolean>,
  "highest_cov_pair": ["<col1>", "<col2>"], 
  "highest_cov_value": <float>
}
```
*Note for `highest_cov_pair`: The column names must be sorted alphabetically (e.g., `["alpha", "beta"]`, not `["beta", "alpha"]`).*

Write and execute the script to produce the final `test_report.json` file.