You are an analyst investigating duplicated records in an ETL pipeline. Due to intermittent failures, some jobs retry and produce duplicate transaction records. 

Your task is to write and execute a Python script at `/home/user/analyze_retries.py` that processes the ETL logs and the transaction data to generate an audit report of affected transactions.

Here are the details and constraints:

1. **Input Files**:
   - `/home/user/etl.log`: A text file containing the execution logs of various ETL jobs. Each line has the format: `TIMESTAMP JOB_ID STATUS` (e.g., `2023-10-01T10:13:00 JOB_B RETRY`).
   - `/home/user/events.csv`: A CSV file containing processed transactions. Columns are `job_id,txn_id,amount`.

2. **Processing Logic**:
   - First, parse `etl.log` to identify all `JOB_ID`s that have a `RETRY` status.
   - Next, parse `events.csv` to find transactions belonging to these retried jobs.
   - **Constraint-based validation**: Only include transactions where the `amount` is an integer strictly greater than or equal to `100`. (Ignore rows with invalid or smaller amounts).
   - **Parallel processing**: You must use Python's `multiprocessing` module (e.g., `multiprocessing.Pool`) to process the CSV data in parallel. 
   - Deduplicate the valid transactions: If a `txn_id` appears multiple times for a retried job (due to the retry), only include it once in the final report.

3. **Outputs**:
   - **Template-based Report**: Generate a file at `/home/user/duplicate_report.txt` exactly matching this template format:
     ```
     Audit Report
     ============
     Total Retried Jobs: {num_retried_jobs}
     Affected Transactions:
     - {txn_id} (Job: {job_id}, Amount: {amount})
     - {txn_id} (Job: {job_id}, Amount: {amount})
     ```
     *Note: Replace `{...}` with actual values. The transactions must be sorted alphabetically by `txn_id`.*
   - **Pipeline Logging**: Your script must log its execution steps to `/home/user/pipeline.log` using Python's built-in `logging` module. It should log at least an `INFO` message when starting and when finishing.

Write the script, run it, and ensure both `/home/user/duplicate_report.txt` and `/home/user/pipeline.log` are generated correctly.