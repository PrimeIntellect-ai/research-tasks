You are a data analyst tasked with processing server access logs using Bash. You must build a multi-stage data processing pipeline entirely from the command line (using Bash, awk, sed, etc., or short inline scripts) to clean, merge, sample, and analyze the data.

You have been provided with two CSV files in the directory `/home/user/data/`:
1. `users.csv` (Columns: `user_id,role,region`)
2. `access_logs.csv` (Columns: `timestamp,ip,user_id,endpoint,status`)

Your objective is to create a shell script at `/home/user/pipeline.sh` that performs the following steps when executed:

**Phase 1: Join and Normalize**
Create a new CSV file at `/home/user/output/normalized_joined.csv` that merges the two files based on `user_id`. 
* The header must be exactly: `timestamp,ip,user_id,role,region,endpoint,status`
* The `endpoint` column must be normalized: convert it to strictly lowercase, and strip any query parameters (everything from the `?` character onwards).
* The output must be sorted chronologically by `timestamp`.

**Phase 2: Stratified Data Sampling**
Create a file at `/home/user/output/stratified_sample.csv`. 
* From the `normalized_joined.csv` data, extract a stratified sample consisting of exactly the *first 2 chronological logs* for each unique `role`. 
* Include the header line at the top.
* The rows (excluding the header) should be sorted alphabetically by `role`, and then chronologically by `timestamp` within each role.

**Phase 3: Anomaly Detection**
We need to find the user who is causing the most errors on the API.
* Analyze the `normalized_joined.csv`.
* Filter for rows where the normalized endpoint starts exactly with `/api/v2/`.
* Count the number of anomaly events per `user_id`. An anomaly is defined as a log entry with a `status` code >= 400.
* Identify the `user_id` with the absolute highest number of anomalies matching this criteria.
* Write ONLY that single `user_id` to `/home/user/output/anomaly_user.txt`. (If there is a tie, write the lowest `user_id`).

**Constraints:**
* All output files must be placed in the `/home/user/output/` directory (which you must create if it doesn't exist).
* `pipeline.sh` must be executable and run the whole end-to-end process without user intervention.
* You may use Bash, awk, sed, join, sort, or Python/Perl if necessary, but the entry point must be the `pipeline.sh` script.