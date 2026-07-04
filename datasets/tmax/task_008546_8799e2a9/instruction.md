You are a Database Reliability Engineer (DBRE) responsible for managing and verifying a hybrid database backup infrastructure. Your backup metadata is stored across two systems: a SQLite database for relational systems and a JSON log file for NoSQL clusters. 

Recently, the backup reporting dashboard has been showing wildly inflated storage metrics. 

You need to complete three critical tasks to fix the reporting pipeline:

**Task 1: Fix the Inflated Metrics Bug**
There is a reporting script at `/home/user/sql_report.sh`. It queries the SQLite database at `/home/user/backups.db` to calculate the total size of successful backups per server. However, it contains a severe SQL bug (an implicit cross join) that multiplies the results.
1. Identify and fix the SQL query inside `/home/user/sql_report.sh` so it correctly joins the `servers` and `backup_jobs` tables.
2. The script must output a strictly formatted CSV to `/home/user/fixed_sql_report.csv` with headers `hostname,total_size_mb`. It should only include servers with successful backups, ordered by total size descending.

**Task 2: Map Backup Dependency Chains**
Incremental backups rely on previous backups. The `backup_lineage` table in the SQLite DB maps `child_id` to `parent_id`. 
1. Write a Bash script at `/home/user/get_chain.sh` that takes a single backup job ID as an argument.
2. Using a Recursive CTE in `sqlite3`, the script must print the entire lineage of that backup job, traversing up to the root (full backup). 
3. The output should be a single line of job IDs separated by `->`, starting from the provided job ID up to the root (e.g., `job105->job102->job100`). Test this script by running it for the job ID `incr_999` and redirecting the output to `/home/user/chain_result.txt`.

**Task 3: NoSQL Backup Aggregation Pipeline**
Your NoSQL backup system outputs logs to `/home/user/nosql_backups.json`.
1. Write a Bash script at `/home/user/nosql_summary.sh` that acts as a NoSQL aggregation pipeline using `jq`.
2. For each `cluster_id`, find the *latest* (highest `timestamp`) backup job where `status` is `"SUCCESS"`.
3. Extract the `cluster_id` and the `size_gb` of that specific job.
4. The script should output a CSV to `/home/user/nosql_report.csv` with headers `cluster_id,latest_size_gb`, sorted alphabetically by `cluster_id`.

Ensure all output files are placed exactly as requested. You have `sqlite3` and `jq` available.