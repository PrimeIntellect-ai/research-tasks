You are acting as a Database Reliability Engineer. We recently restored a backup verification environment consisting of a SQLite database and a JSON file containing NoSQL-style backup dependency documents. 

However, our previous verification process is broken. You need to write a script in the language of your choice to perform the following tasks:

1. **Fix the Implicit Cross Join & Optimize DB**:
   We have a SQLite database at `/home/user/backups.db` with two tables:
   - `servers` (`id` INTEGER, `hostname` TEXT)
   - `backups` (`id` INTEGER, `server_id` INTEGER, `timestamp` INTEGER, `size_bytes` INTEGER, `status` TEXT)
   
   A junior engineer tried to write a query to get the total size of all 'SUCCESS' backups for a specific server hostname ('db-prod-01'), but wrote this:
   `SELECT SUM(b.size_bytes) FROM servers s, backups b WHERE s.hostname = 'db-prod-01' AND b.status = 'SUCCESS';`
   This is returning an inflated number due to an implicit cross join.
   - You must execute the correct SQL query to find the sum of `size_bytes` for all 'SUCCESS' backups belonging strictly to the server with `hostname` = 'db-prod-01'.
   - You must also create appropriate index(es) on the `backups` table in the SQLite database to optimize this query.

2. **Graph Traversal for Restoration Plan**:
   There is a JSON file at `/home/user/dependency_graph.json` which contains an array of documents representing incremental backups. Each document has the format:
   `{"backup_id": <int>, "depends_on": [<list of backup_ids>], "restore_time_minutes": <int>}`
   - You must compute the shortest restoration time (minimum total `restore_time_minutes`) required to fully restore `backup_id` 50 starting from `backup_id` 1. A valid path must start at `backup_id` 1, traverse through the `depends_on` relationships (if A depends on B, you can transition from B to A), and end at `backup_id` 50. The total time is the sum of `restore_time_minutes` for all nodes in the path (including the start and end nodes).

3. **Output**:
   Write your final results to a file at `/home/user/report.txt` with exactly the following format:
   ```
   Total Backup Size: <corrected_sum_of_size_bytes>
   Shortest Restore Time: <min_total_minutes>
   ```

You are free to use any programming language (Python, Node.js, bash+sqlite3+jq, etc.) to accomplish this task.