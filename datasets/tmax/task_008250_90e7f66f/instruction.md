You are a Database Reliability Engineer. We have an SQLite database containing metadata about our automated database backups at `/home/user/backup_metadata.db`. 

We need to identify "at-risk" database clusters based on recent backup performance and reliability. 

Your task is to write a C++ program (`/home/user/analyze_backups.cpp`) that queries this SQLite database, processes the results, and generates a CSV report of at-risk clusters.

### Database Schema
The SQLite database has two tables:
1. `clusters`
   - `id` (INTEGER PRIMARY KEY)
   - `name` (TEXT)
2. `backups`
   - `id` (INTEGER PRIMARY KEY)
   - `cluster_id` (INTEGER, foreign key to clusters)
   - `timestamp` (INTEGER, Unix epoch)
   - `duration_sec` (INTEGER)
   - `status` (TEXT, either 'SUCCESS' or 'FAILED')

### Risk Criteria
A cluster is considered "at-risk" if it meets AT LEAST ONE of the following criteria:
1. The *most recent* backup (by timestamp) for that cluster has a status of 'FAILED'.
2. The duration of the *most recent* 'SUCCESS' backup is strictly greater than 1.5 times the average duration of the **3** 'SUCCESS' backups immediately preceding it (ordered by timestamp descending). *Note: If a cluster has fewer than 4 'SUCCESS' backups total, do not flag it under this specific criteria.*

### Requirements
1. Install any necessary dependencies to compile C++ code with SQLite3.
2. Write a C++ program at `/home/user/analyze_backups.cpp` that connects to `/home/user/backup_metadata.db`.
3. Use SQL window functions, joins, and subqueries as much as possible to compute the required metrics efficiently.
4. The C++ program must output a CSV file at `/home/user/at_risk_clusters.csv` containing the names of the at-risk clusters, sorted alphabetically.
5. The CSV should have a single column with the header `cluster_name`.
6. Compile your program to `/home/user/analyze_backups` and run it to produce the output file.