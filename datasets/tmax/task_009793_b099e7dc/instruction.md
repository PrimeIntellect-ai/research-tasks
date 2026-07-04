You are a Database Reliability Engineer (DBRE) tasked with optimizing our database backup schedules. We have a complex microservice architecture where some databases must be backed up before others to maintain referential integrity in our data warehouse. 

An automated tool has exported our backup dependencies into a CSV file located at `/home/user/backup_deps.csv`. The file has the header `source_db,target_db,job_id`. A row indicates that `source_db` must be backed up before `target_db` as part of `job_id`.

Your task is to write a C program at `/home/user/analyze_backups.c` that performs graph analytics to find the most "critical" databases—those that serve as the foundation for the most downstream backups.

The C program must:
1. Parse the CSV file `/home/user/backup_deps.csv` (skipping the header row).
2. Map the relationships to calculate the out-degree for each `source_db` (i.e., the total number of outgoing edges/dependencies it has to any `target_db`).
3. Aggregate and summarize these counts.
4. Output the top 3 most critical databases (highest out-degree) to a file named `/home/user/critical_backups.txt`.
5. The output format in `/home/user/critical_backups.txt` must be exactly 3 lines, formatted as `dbname: count`.
6. If there is a tie in the count, sort the tied databases alphabetically by their name.

Once you have written the code, compile it using `gcc` and run it to generate the `/home/user/critical_backups.txt` file. Make sure the output file is created successfully and matches the required format exactly.