You are a log analyst investigating patterns in a newly deployed application. The application generates messy, unstructured log files. Your task is to build a Bash-based ETL (Extract, Transform, Load) pipeline that tokenizes the log entries, normalizes the data, extracts specific features, bulk imports them into a database, and sets up a scheduled job.

You have been provided a raw log file at `/home/user/incoming.log`. 
Each line in this log file represents an event, but the key-value pairs are out of order, and the casing is inconsistent. 

Example log lines:
`[2024-05-12T08:15:30] LEVEL=warn msg="Disk space low" IP=192.168.1.5 user=AdminCode code=404`
`[2024-05-12T08:16:05] ip=10.0.0.9 CODE=500 level=ERROR msg="Crash" USER=sysadmin`

Your objectives are:

1. **Write an ETL script (`/home/user/etl.sh`):**
   Create a Bash script that takes two arguments: an input log file path and an output CSV file path.
   - The script must parse each line to extract the following 5 fields: `timestamp`, `level`, `code`, `user`, and `ip`.
   - The `timestamp` is always enclosed in brackets `[...]` at the beginning of the line. Extract the timestamp without the brackets.
   - Extract the values for `level`, `code`, `user`, and `ip` using Bash commands (`awk`, `sed`, `grep`, etc.).
   - **Normalization rules:** 
     - `level` must be converted to fully UPPERCASE.
     - `user` must be converted to fully lowercase.
     - If `user`, `ip`, or `code` are missing from a line, use the string `NULL` in the CSV.
   - The script should generate a headerless CSV with the exact order: `timestamp,level,code,user,ip`.
   - After generating the CSV, the script must bulk import this CSV into a SQLite database located at `/home/user/metrics.db` into a table named `incidents`. 
     - The table schema should be: `timestamp TEXT, level TEXT, code INTEGER, user TEXT, ip TEXT`.
     - (Note: Ensure the table is created if it does not exist, and clear any existing data in the table before bulk importing so it only contains the latest run's data).

2. **Run the script:**
   Execute your script to process `/home/user/incoming.log` and output to `/home/user/parsed.csv`. Ensure the data successfully imports into `/home/user/metrics.db`.

3. **Pipeline Scheduling:**
   Create a cron job that runs your script (`/home/user/etl.sh /home/user/incoming.log /home/user/parsed.csv`) exactly at minute 15 of every hour. 
   - Install this cron job for the `user`.
   - Also, save the exact cron expression and command as a single line in `/home/user/cron_schedule.txt`.

Ensure `/home/user/etl.sh` is executable. You may assume `sqlite3` and standard Linux utilities (`awk`, `sed`, `tr`, etc.) are installed.