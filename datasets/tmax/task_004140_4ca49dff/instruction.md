You are a Database Reliability Engineer investigating backup chain integrity. We have an SQLite database tracking server backups, but an infrastructure failure corrupted one of its indexes, causing queries to return stale or missing rows. 

Your task is to write a Python script `/home/user/analyze_chains.py` that analyzes the backup chains, bypassing the corruption, and outputs a summarized report.

**Database Path:** `/home/user/backups.db`

**Schema:**
1. `servers` table:
   - `server_id` (INTEGER PRIMARY KEY)
   - `hostname` (TEXT)
2. `jobs` table:
   - `job_id` (INTEGER PRIMARY KEY)
   - `server_id` (INTEGER)
   - `parent_id` (INTEGER) - Links to a previous `job_id` (used for incremental backups). NULL for FULL backups.
   - `size_bytes` (INTEGER)
   - `type` (TEXT) - 'FULL' or 'INC'

**The Problem & Requirements:**
1. **Corrupted Index:** The `jobs` table has an index `idx_parent` on the `parent_id` column. Because this index is corrupted, you **must** instruct SQLite to ignore it to get accurate results. Use the SQLite `NOT INDEXED` clause when querying the `jobs` table.
2. **Graph Projection:** A backup "chain" consists of a root FULL backup (`parent_id` IS NULL) and all of its recursive descendants (incremental backups that depend on it, or depend on a job that depends on it).
3. **Aggregation:** For each chain, calculate:
   - The `root_job_id` (the ID of the FULL backup).
   - The `total_size` (sum of `size_bytes` of the FULL backup and all its recursive descendants).
   - The `job_count` (total number of backup jobs in this chain).
4. **Filtering:** Only include chains where the `total_size` is strictly greater than `5000` bytes.
5. **Output:** Write the results to `/home/user/chain_report.json` as a JSON dictionary mapping `hostname` to a list of its valid chain summaries. 
   - The lists of chain summaries must be sorted by `root_job_id` in ascending order.
   - Example format:
     ```json
     {
       "db-prod-01": [
         {
           "root_job_id": 1,
           "total_size": 5500,
           "job_count": 3
         }
       ]
     }
     ```

Write and execute the Python script to produce the final `chain_report.json` file.