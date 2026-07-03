You are a Database Reliability Engineer. You have been tasked with analyzing a complex failure in our database backup systems. Our infrastructure consists of primary databases and their read-replicas. Backups are taken for both.

You have two data sources:
1. `/home/user/backups.json`: A document store export containing backup metadata. Format: `[{"id": "b1", "db_instance": "db-primary-1", "status": "success", "size_gb": 100}, ...]`
2. `/home/user/replication_graph.csv`: A CSV file representing the replication topology (directed graph from primary to replica). Format: `primary,replica`

Your goal is to write a bash script at `/home/user/analyze_backups.sh` (make it executable) that analyzes these files and generates a summary report at `/home/user/report.csv`.

The report must identify all **primary databases** that have *at least one replica* whose backup failed.
For each such primary database, calculate:
1. The total number of replicas attached to it (its out-degree in the replication graph).
2. The total size (in GB) of all *successful* backups for its entire cluster (the primary itself plus all of its replicas).

The output `/home/user/report.csv` must contain no headers, be sorted alphabetically by the primary database name, and use the following comma-separated format:
`Primary_Database_Name,Number_Of_Replicas,Total_Successful_Backup_Size_GB`

Constraints:
- You must use standard shell tools (bash, awk, jq, grep, join, sort, etc.). Do not use Python, Perl, or external database engines.
- Assume standard GNU coreutils and `jq` are available.

Example output line in `/home/user/report.csv`:
`db-primary-1,2,150`