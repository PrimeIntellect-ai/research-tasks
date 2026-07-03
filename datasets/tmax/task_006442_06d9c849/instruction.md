You are a log analyst investigating a complex pattern of errors cascading from our web servers to our databases. You have been provided with two log files:
1. `/home/user/web_logs.csv` (Columns: `timestamp`, `ip_address`, `status_code`, `endpoint`, `error_msg`, `req_id`)
2. `/home/user/db_logs.csv` (Columns: `timestamp`, `user_email`, `db_error`, `req_id`)

Your objective is to write and run a Python script that correlates these logs, filters the noise, and outputs a clean, anonymized report.

Perform the following steps exactly as described:

1. **Stratified Extraction:**
   Read `/home/user/web_logs.csv`. For each unique `status_code`, extract exactly the first 20 rows (reading from top to bottom). If a status code has fewer than 20 rows, extract all of them.

2. **Join and Similarity Computation (Parallelized):**
   For each extracted web log entry, find all entries in `/home/user/db_logs.csv` that have the exact same `req_id`. 
   Compute the Levenshtein edit distance between the web log's `error_msg` and the database log's `db_error`.
   Keep only the joined pair that has the minimum edit distance, and ONLY if that edit distance is strictly less than 15.
   *Requirement:* You must use Python's `multiprocessing` or `concurrent.futures` to parallelize this distance computation and join phase. You may use the `Levenshtein` library.

3. **Data Masking:**
   For the successfully matched pairs, you must mask the PII:
   - `ip_address`: Replace the last two octets with `*.*` (e.g., `192.168.1.100` becomes `192.168.*.*`).
   - `user_email`: Keep the first letter of the username, replace the rest of the username with four asterisks `****`, and keep the domain intact (e.g., `johndoe@example.com` becomes `j****@example.com`).

4. **Output Generation:**
   Save the final processed data to `/home/user/investigation_results.jsonl`. 
   Each line should be a valid JSON object with the following exact keys:
   `req_id`, `status_code`, `masked_ip`, `masked_email`, `web_error`, `db_error`, `edit_distance`.
   The file must be sorted in ascending order by `req_id` (alphabetically).

Write your code, install any necessary libraries (e.g., `pip install Levenshtein`), and execute your pipeline to produce the output file.