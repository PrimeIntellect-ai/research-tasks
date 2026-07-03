You are a Database Reliability Engineer (DBRE) investigating a potential storage cost anomaly in our backup infrastructure. Our backup pipelines replicate data across a complex topology of servers, SANs, and cloud buckets.

I have provided a SQLite database at `/home/user/backups.db` containing two tables:
1. `topology`: Represents the directed knowledge graph of backup replication.
   - `source_node` (TEXT): The node where data originates.
   - `target_node` (TEXT): The node where data is replicated to.
2. `jobs`: Contains metadata about individual backup runs.
   - `job_id` (TEXT): Unique identifier for the backup job.
   - `node` (TEXT): The node storing this backup.
   - `run_date` (TEXT): ISO8601 timestamp of the backup.
   - `size_mb` (REAL): Size of the backup in megabytes.
   - `status` (TEXT): 'SUCCESS' or 'FAILED'.

Your task is to write and execute a SQL query (using `sqlite3`) that identifies anomalous backup sizes for all nodes that are downstream of the primary database `db-main` (including `db-main` itself).

Specifically, you must:
1. Use graph pattern matching (a Recursive CTE) to find all nodes reachable from `source_node = 'db-main'` in the `topology` table.
2. For all 'SUCCESS' jobs on these downstream nodes, calculate a 3-period rolling average of `size_mb`. This rolling average should be calculated partitioned by `node`, ordered by `run_date` ascending, including the current row and the 2 preceding rows.
3. Isolate the **most recent** successful backup job for each downstream node.
4. Filter the results to only include nodes where this most recent backup's `size_mb` is strictly greater than 1.5 times its 3-period rolling average.
5. Sort the final output by `size_mb` in descending order.

Save the output to `/home/user/anomaly_report.csv` with `|` as the delimiter (standard sqlite3 list output). The file should have exactly four columns in this order, with no headers:
`node|job_id|size_mb|rolling_avg`
(Note: round the `rolling_avg` to 2 decimal places in your final output).