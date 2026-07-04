You are acting as a compliance officer auditing an internal system. 

We have an SQLite database located at `/home/user/audit.db` containing a single table `access_logs` with the following schema:
`CREATE TABLE access_logs (id INTEGER PRIMARY KEY, user_id INTEGER, ip_address TEXT, login_time DATETIME, logout_time DATETIME);`

Your task is to write a Bash script at `/home/user/audit_check.sh` that automates a compliance check to detect suspicious session overlaps. The script must perform the following actions exactly:

1. Connect to `/home/user/audit.db` and create a covering index named `idx_user_login` on the `user_id` and `login_time` columns to optimize the analytical query you are about to run.
2. Execute a SQL query that uses Window Functions to identify "suspicious overlapping sessions." 
   - A session is considered a "suspicious overlap" if a user's `login_time` occurs *strictly before* the `logout_time` of their *immediately preceding* session (when ordered by `login_time` for that specific `user_id`), AND the `ip_address` of the current session is strictly different from the `ip_address` of that immediately preceding session.
3. Export the results of this query into a CSV file located at `/home/user/suspicious_overlaps.csv`.
4. The CSV must contain headers and precisely these columns in this order: `user_id`, `first_ip`, `second_ip`, `overlap_start_time`. 
   - `first_ip`: The IP address of the preceding session.
   - `second_ip`: The IP address of the newly overlapping session.
   - `overlap_start_time`: The `login_time` of the newly overlapping session.

Ensure your script is executable (`chmod +x /home/user/audit_check.sh`) and runs successfully without interactive prompts.