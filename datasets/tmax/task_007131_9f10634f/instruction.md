You are a Database Reliability Engineer. We have a backup verification system that reads metadata from a SQLite database (`/home/user/backup_meta.db`) to generate reports. 

A previous engineer left behind a broken export script at `/home/user/export.sh`. The script contains a SQL query that exports data to CSV, but it suffers from a severe implicit cross join, resulting in massively duplicated and incorrect rows. Furthermore, it doesn't filter out failed backups.

Your task consists of the following phases:

1. **Reverse Engineer the Schema:**
   Inspect `/home/user/backup_meta.db` to understand the relationships between the `databases`, `tables`, and `backups` tables. 

2. **Fix the Query:**
   Rewrite the SQL query to correctly join the three tables using their actual relational mappings. Additionally, ensure the query ONLY selects rows where the backup `status` is exactly `'SUCCESS'`. The output columns must be exactly in this order: `database_name`, `table_name`, `backup_date`.

3. **Create a C Result Processor:**
   Write a C program at `/home/user/processor.c` and compile it to `/home/user/processor`. This program must:
   - Read the CSV formatted output (no header) from standard input (`stdin`).
   - Parse the three columns: `db_name`, `table_name`, `backup_date`.
   - Output a formatted string to standard output (`stdout`) for each row in the exact format: `[backup_date] db_name::table_name`.

4. **Construct the Pipeline:**
   Create a bash script at `/home/user/run_pipeline.sh` that:
   - Uses `sqlite3` to execute your fixed query against `/home/user/backup_meta.db` in CSV mode (without headers).
   - Pipes the output directly into your compiled `/home/user/processor`.
   - Redirects the final formatted output to `/home/user/backup_report.txt`.

Ensure all files (`processor.c`, `processor`, `run_pipeline.sh`, and `backup_report.txt`) are created and have the correct permissions. Run `/home/user/run_pipeline.sh` to generate the final report.