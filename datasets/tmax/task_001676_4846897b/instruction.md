As a Database Reliability Engineer, you have inherited an undocumented SQLite database containing backup execution metadata at `/home/user/backups.db`. 

Your task is to analyze the database and write a Go program to extract a specific analytical report.

Requirements:
1. Reverse engineer the SQLite database schema to understand how backup jobs and their parent-child dependencies are stored.
2. Write a Go program at `/home/user/generate_report.go` that queries this database.
3. Your SQL query must use a **recursive CTE** to find the job named `'full_cluster_backup'` and all of its direct and indirect descendant jobs.
4. For only this hierarchical subset of jobs, use a **window function** to calculate each job's size rank within its respective backup suite (the largest backup in a suite gets rank 1, using standard ranking where ties get the same rank).
5. The Go program must execute this query and write the results to `/home/user/report.csv` with the exact header: `job_name,suite_id,size_bytes,size_rank`.
6. The CSV output must be sorted by `suite_id` ascending, then `size_rank` ascending, then `job_name` ascending.

Environment setup:
- Run `go mod init backup_report` and `go get github.com/mattn/go-sqlite3` in `/home/user/` to set up your Go module.
- Compile and run your program to produce the `/home/user/report.csv` file.

Do not hardcode the expected data into your Go program; your program must compute it dynamically by querying the database.