You are acting as a data engineer assisting a data scientist. We receive daily dumps of user data and activity logs that need to be cleaned, deduplicated, and merged before analysis. 

Your task is to build a data pipeline that processes these files. You must write a bash wrapper script `/home/user/run_pipeline.sh` that coordinates the execution, and you can write additional scripts in Python, awk, or bash to perform the processing.

Here are the requirements:

1. **Input Data**:
   - `/home/user/data/users.csv`: A CSV with headers `id,name,email,join_date`. The data is messy.
   - `/home/user/data/activity.jsonl`: A JSON Lines file where each line is an object like `{"user_email": "...", "action": "login"}`.

2. **Normalization and Standardization**:
   - For `users.csv`: 
     - Convert the `email` field to entirely lowercase.
     - Convert the `name` field to Title Case (e.g., "john DOE" -> "John Doe").
     - Standardize `join_date` to `YYYY-MM-DD` format (inputs might be `MM/DD/YYYY` or `YYYY-MM-DD`).

3. **Hash-based Deduplication**:
   - After normalizing the users, deduplicate the records. If multiple rows have the same MD5 hash for their normalized `email`, keep ONLY the first occurrence (based on the original file order) and drop the rest.

4. **Joins and Merges**:
   - Calculate the total number of activities for each user from `activity.jsonl` (matching on the normalized lowercase email).
   - Produce a final merged CSV file at `/home/user/output/clean_merged.csv` with the headers exactly as: `id,name,email,join_date,activity_count`. If a user has no activities, their `activity_count` should be `0`. The order of rows must match the deduplicated users.

5. **Pipeline Logging**:
   - The `/home/user/run_pipeline.sh` script must append a log line to `/home/user/pipeline.log` upon successful completion. 
   - The log line must exactly match this format: `[YYYY-MM-DD HH:MM:SS] SUCCESS: Processed <N> unique users.` where `<N>` is the final number of rows written to `clean_merged.csv` (excluding the header).

6. **Pipeline Scheduling**:
   - Install a cron job for the `user` that executes `/home/user/run_pipeline.sh` every day at 2:30 AM.

Constraints:
- Create the `/home/user/output` directory if it does not exist.
- Ensure `/home/user/run_pipeline.sh` is executable.
- Run `/home/user/run_pipeline.sh` once manually so the output files and logs are generated.