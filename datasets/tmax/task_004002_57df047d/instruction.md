You are an MLOps engineer investigating a silent data corruption issue in your experiment tracking directory located at `/home/user/experiments/`. 

Due to a faulty pandas pipeline, some classification experiment artifacts had their integer predictions silently converted to floats or `NaN` values. Other experiments in the directory are regression tasks containing legitimate continuous predictions.

Your task is to use standard Bash tools (like `awk`, `grep`, `shuf`, etc.) to clean the data, perform a bootstrap sample, and evaluate the model.

Perform the following steps exactly as specified:

1. **Filter Valid Experiments**: Inspect `predictions.csv` in each `run_*` directory inside `/home/user/experiments/`. A valid classification run is one where the `prediction` column (the second column, comma-separated) strictly contains only the characters `0` or `1` (excluding the header `true_label,prediction`). Runs containing floats (like `1.0`), continuous values, or `NaN` should be ignored.
2. **Pool the Data**: Extract the data rows (excluding headers) from all valid classification runs and combine them into a single file at `/home/user/pooled_preds.csv`.
3. **Bootstrap Sampling**: Generate a bootstrap sample (random sampling *with replacement*) of exactly 500 rows from `pooled_preds.csv`. Save this sample to `/home/user/bootstrap_sample.csv`. You must use the `shuf` command for this step.
4. **Evaluate**: Calculate the classification accuracy (the proportion of rows where `true_label` equals `prediction`) of your `bootstrap_sample.csv`. 
5. **Report**: Write the final calculated accuracy (as a decimal between 0 and 1, e.g., `0.842`) into `/home/user/report.txt`.

Ensure your commands are executed in a standard Bash shell. You do not need root access for this task.