You are a Database Reliability Engineer (DBRE) tasked with managing and optimizing backup routing across our multi-region database infrastructure. 

You have been provided with an SQLite database at `/home/user/backups.db` containing three tables:
1. `nodes` (`node_id` TEXT PRIMARY KEY, `region` TEXT)
2. `backups` (`backup_id` TEXT PRIMARY KEY, `node_id` TEXT, `size_gb` INTEGER)
3. `network_links` (`source` TEXT, `target` TEXT, `latency_ms` INTEGER)

There is a Python script at `/home/user/report.py` that is supposed to generate a backup storage report, but it contains a critical bug. The junior engineer who wrote it used an implicit cross join, resulting in wildly inaccurate total backup sizes.

Your task is to fix and expand the script `/home/user/report.py` to correctly calculate the metrics and output them to `/home/user/report_output.txt`. 

You must modify the script to perform three specific tasks using Python's `sqlite3` library:

**Task 1: Correct Total Backup Size Calculation**
Fix the query to correctly join `nodes` and `backups` to calculate the total `size_gb` of all backups per region. Sort the output alphabetically by region. 

**Task 2: Top 2 Backups per Region**
Write a query using a SQL Window Function to find the top 2 largest backups (by `size_gb`) within each region. If there are ties, sort by `backup_id` ascending. Exclude regions with no backups. Sort the final regions alphabetically, and within each region sort by the size descending.

**Task 3: Shortest Transfer Path**
We need to transfer a critical archive from node `A` to node `F`. The `network_links` table represents a directed graph of network connections. Write a Recursive CTE in SQLite to compute the shortest path (minimum total `latency_ms`) from `source` 'A' to `target` 'F'. 

**Output Format Specification:**
Your Python script must execute these queries and write the exact following format to `/home/user/report_output.txt`:

```
--- Total Size Per Region ---
[Region]: [Total Size] GB
...
--- Top 2 Backups Per Region ---
[Region] - [backup_id]: [size_gb] GB
...
--- Shortest Path A to F ---
Total Latency: [latency] ms
```
Do not install any external Python libraries; use standard library modules only (e.g., `sqlite3`). Create and run the script to generate the output file.