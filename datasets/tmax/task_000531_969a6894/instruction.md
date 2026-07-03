You are an MLOps engineer analyzing tracking logs for various model experiments. You have two CSV files containing experiment metadata and evaluation metrics. You need to join these files, enforce data quality constraints, engineer a new metric, and aggregate the results using only standard Linux command-line tools (Bash, awk, sort, join, etc.).

Your input files are:
1. `/home/user/models.csv` - Contains model metadata. Format: `model_id,model_type,hyperparams`
2. `/home/user/evals.csv` - Contains evaluation runs. Format: `model_id,run_id,accuracy,loss`

Perform the following data processing steps:
1. **Join**: Combine the data from both files based on the `model_id`.
2. **Schema Enforcement**: Filter out any rows where `accuracy` or `loss` are invalid. To be valid:
   - `accuracy` must be a number between `0.0` and `1.0` (inclusive).
   - `loss` must be a number strictly greater than `0.0`.
   - Ignore any rows with non-numeric strings in these columns (like "err" or "NaN").
3. **Feature Engineering**: For each valid evaluation run, compute the `efficiency_score` as `accuracy / loss`.
4. **Aggregation**: For each `model_type`, calculate:
   - The total number of valid runs.
   - The mean `efficiency_score` across all valid runs.

Output the final aggregated metrics to a file named `/home/user/report.csv`. 
The file must have the following exact specifications:
- A header row: `model_type,run_count,mean_efficiency`
- Comma-separated columns.
- `mean_efficiency` formatted to exactly 4 decimal places (e.g., `4.5694`).
- Sorted in descending order of `mean_efficiency`.

Do not write external Python or R scripts. Rely purely on shell utilities (like `awk`, `join`, `sort`, `sed`, etc.).