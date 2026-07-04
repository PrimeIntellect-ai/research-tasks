You are a log analyst investigating patterns in server performance logs. The system monitoring agent recently malfunctioned, resulting in a corrupted metrics log file. Your task is to build a robust, orchestrated data processing pipeline entirely in Bash (using standard tools like `awk`, `sed`, `grep`, etc.) to clean, impute, and extract aggregated features from this data.

The raw data is located at `/home/user/workspace/raw_metrics.csv`.
It has a header and comma-separated values: `timestamp,server_id,cpu_usage,mem_usage,status_code`.

You must create a pipeline consisting of three processing scripts and one orchestration script in `/home/user/workspace/`.

**Phase 1: Validation and Filtering (`1_filter.sh`)**
1. Read `raw_metrics.csv`.
2. Keep the header row.
3. Filter out any rows where `status_code` is NOT one of the following valid HTTP-like codes: `200`, `301`, `404`, `500`.
4. **Validation Checkpoint:** After filtering, the script must count the number of data rows (excluding the header). If the count is less than 10, the script must print "Quality Gate Failed: Insufficient Data" to standard error and exit with a non-zero status code (e.g., `exit 1`).
5. Save the valid rows to `filtered.csv`.

**Phase 2: Imputation (`2_impute.sh`)**
The monitoring agent occasionally failed to record `cpu_usage` or `mem_usage`, placing a `-` (dash) character instead.
1. Read `filtered.csv`.
2. Keep the header row.
3. Perform a **forward-fill imputation** per `server_id`. If a row has a `-` for `cpu_usage` or `mem_usage`, replace it with the last known valid value for that specific `server_id`.
   *(Assume the first log entry for any server will always have valid metrics, never a `-`).*
4. Save the imputed rows to `imputed.csv`.

**Phase 3: Feature Extraction and Aggregation (`3_aggregate.sh`)**
1. Read `imputed.csv`.
2. Calculate the average `cpu_usage` and average `mem_usage` for each `server_id`.
3. Save the results to `summary.csv` without a header.
4. The output must be formatted strictly as `server_id,avg_cpu,avg_mem`.
5. The average values must be rounded to exactly two decimal places (e.g., `45.50`).
6. Sort the final output alphabetically by `server_id`.

**Phase 4: DAG Orchestration (`run_pipeline.sh`)**
1. Create a master script `run_pipeline.sh` that executes the three scripts in order.
2. It must enforce the pipeline DAG: if any script exits with a non-zero code, the pipeline must immediately abort, print "Pipeline Failed at step X" (where X is the step number), and exit with code `1`.
3. If all steps succeed, it should print "Pipeline Success" and exit with code `0`.

Run your `run_pipeline.sh` script to generate the final `summary.csv`. Do not leave the final output file empty or incorrectly formatted. Ensure your scripts are executable.