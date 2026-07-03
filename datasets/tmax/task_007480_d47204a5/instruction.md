You are an automation specialist dealing with a broken ETL workflow. The ETL job periodically ingests transaction logs but frequently retries upon network failures, resulting in exact duplicate records. Furthermore, upstream bugs have introduced malformed records, inconsistent formatting, and anomalous values. 

Your task is to write a Bash script at `/home/user/etl_cleaner.sh` that processes a directory of raw CSV files and produces clean, deduplicated, and anomaly-flagged datasets.

**Input Data:**
- Location: Multiple CSV files in `/home/user/data/` (e.g., `etl_run_1.csv`, `etl_run_2.csv`).
- Format: `timestamp,user_id,action,value` (No headers).

**Requirements for `/home/user/etl_cleaner.sh`:**
The script must take no arguments, read from `/home/user/data/*.csv`, and produce exactly two output files: `/home/user/cleaned.csv` and `/home/user/anomalies.csv`. 

It must perform the following pipeline in order:

1. **Tokenization and Normalization:**
   - The `action` column often contains leading/trailing whitespace and mixed case (e.g., ` PuRchase `). 
   - Strip all whitespace from the `action` column and convert it to strictly lowercase.

2. **Constraint-Based Validation:**
   - Discard any record that does not meet ALL the following constraints:
     - `timestamp` must exactly match ISO 8601 UTC format: `YYYY-MM-DDTHH:MM:SSZ`.
     - `user_id` must be exactly 6 alphanumeric characters (e.g., `usr123`).
     - `action` (after normalization) must be exactly `purchase`, `refund`, or `login`.
     - `value` must be a non-negative integer (digits only).

3. **Deduplication and Timestamp Alignment:**
   - Remove any exact duplicate records (after normalization).
   - Sort all remaining records chronologically by `timestamp` (ascending).

4. **Anomaly and Changepoint Detection:**
   - Process the sorted, deduplicated records.
   - For each unique `user_id`, track their "baseline" value. 
   - The baseline is the `value` of their most recent *valid, non-anomalous* transaction where the action is either `purchase` or `refund`. (Ignore `login` actions for baseline calculations).
   - A transaction (`purchase` or `refund`) is considered an **anomaly** if its `value` is strictly greater than 10 times that user's current baseline.
   - The first `purchase` or `refund` for a user is never an anomaly.
   - If a record is an anomaly, it *does not* update the baseline.

5. **Output:**
   - Write all valid, non-anomalous records to `/home/user/cleaned.csv`.
   - Write all detected anomalies to `/home/user/anomalies.csv`.
   - Both output files must maintain the chronological sort order and use the normalized CSV format (`timestamp,user_id,action,value`).

Make sure your script is executable (`chmod +x /home/user/etl_cleaner.sh`). Run your script to generate the final output files before completing the task.