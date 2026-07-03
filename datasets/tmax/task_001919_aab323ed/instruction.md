You are an MLOps engineer tasked with analyzing experiment metrics using only native Linux command-line tools. You have a dataset of experiment artifacts located at `/home/user/artifacts.csv`. This CSV contains 100 rows of telemetry from different model runs, with columns: `run_id,latency_ms,cpu_usage_pct,memory_mb,validation_loss`.

Your goal is to write a pure Bash script (using standard utilities like `awk`, `shuf`, `bc`, etc. - no Python or R) located at `/home/user/analyze_artifacts.sh` that performs the following steps:

1. **Dimensionality Reduction (Feature Selection):** Parse the CSV (ignoring the header and the `run_id` column) and calculate the statistical variance for each of the 4 metric columns. Identify the column name with the highest variance. This is our primary feature of interest.
2. **Bootstrap Sampling:** For this highest-variance column, perform a bootstrap analysis to estimate the mean. Generate $B=1000$ bootstrap samples. Each bootstrap sample is created by sampling 100 values *with replacement* from the selected column. Calculate the mean of each bootstrap sample.
3. **Numerical Accuracy Testing:** Calculate the true mean of the highest-variance column. Then, calculate the grand mean of your 1000 bootstrap means. Test if the absolute difference between the true mean and the grand bootstrap mean is strictly less than `0.5`.
4. **Reporting:** The script must output a summary report to `/home/user/artifact_report.txt` in the following exact format:
```
Primary Feature: <column_name>
True Mean: <value rounded to 2 decimal places>
Bootstrap Grand Mean: <value rounded to 2 decimal places>
Accuracy Check Passed: <Yes/No>
```

For the accuracy check, output "Yes" if the absolute difference is < 0.5, otherwise "No".
Assume the first row of `artifacts.csv` is the header. Do not use external scripting languages like Python, Perl, or Ruby. You may use `awk` heavily. Make sure `/home/user/analyze_artifacts.sh` has execute permissions. Run your script to generate the report.