You are an MLOps engineer tasked with building a pure-Bash ETL and testing pipeline to track experiment artifacts and clean messy training logs.

Your system does not have `jq` installed by default, and you lack root (sudo) access. 

First, configure your environment:
1. Download the `jq` binary (version 1.6) for linux64 from its official GitHub releases.
2. Install it locally into `/home/user/bin/jq` and ensure it is executable.

Second, construct an ETL pipeline:
You have a raw metrics file located at `/home/user/ml_metrics.csv` with the following header:
`run_id,epoch,loss,accuracy`

Write a Bash script at `/home/user/process_metrics.sh` that processes this CSV file based on the following rules:
1. **Missing Value Handling**: If the `loss` column is empty, impute it with the exact string `0.500`.
2. **Outlier Handling**: Filter out (drop) any rows where `accuracy` is strictly greater than `1.0` or strictly less than `0.0`.
3. **Data Transformation**: Skip the header row. For all valid rows, use standard Bash tools (like `awk`) and your newly installed `jq` to output a single JSON array containing objects for each retained row. 
4. The output must be saved to `/home/user/cleaned_metrics.json`. Each object in the JSON array must have the exact keys: `"run"` (string, from run_id), `"loss"` (number), and `"acc"` (number, from accuracy).

Third, build a test script:
Write a test script at `/home/user/test_pipeline.sh` that validates your pipeline's output. The test script must:
1. Check if `/home/user/cleaned_metrics.json` exists.
2. Use `jq` to count the number of elements in the JSON array.
3. Print exactly: `Test passed: <N> valid records found.` (where `<N>` is the counted number).
4. Save the output of this test script to `/home/user/test_results.log`.

Execute your scripts so that `/home/user/cleaned_metrics.json` and `/home/user/test_results.log` are generated and correctly populated.