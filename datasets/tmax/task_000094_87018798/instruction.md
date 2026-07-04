You are a Database Reliability Engineer investigating a series of backup failures. The backup metadata is stored in a local SQLite database at `/home/user/backups.db`.

We use a hierarchical backup strategy: a "Full" backup is taken, followed by "Incremental" backups that reference their parent backup. 
The `backups` table has the following schema:
`CREATE TABLE backups (id INTEGER PRIMARY KEY, parent_id INTEGER, status TEXT, timestamp INTEGER);`
`CREATE INDEX idx_status_time ON backups(status, timestamp);`

Recently, the database suffered block-level corruption affecting the `idx_status_time` index. Queries using this index return stale or missing rows. 

Your task is to write a Python script at `/home/user/analyze_backups.py` that connects to this database and extracts specific backup chains. 

Requirements for the script:
1. **Bypass the Corruption**: You MUST ensure your query does not use the corrupted index. Modify your SQL query to explicitly bypass it (e.g., using SQLite's `NOT INDEXED` clause on the `backups` table) so it forces a full table scan. Do not drop the index or modify the database schema.
2. **Hierarchical Query**: Use a Recursive CTE (`WITH RECURSIVE`) to reconstruct the full backup chains. A chain starts with a root backup (`parent_id IS NULL`) and includes all its descendants. 
3. **Filter**: We only care about backup chains where *at least one* backup in the chain has `status = 'FAILED'`.
4. **Sort and Paginate**: Order these failed chains descending by the `timestamp` of their *root* (Full) backup. We want to retrieve exactly "Page 2" of the results, assuming a page size of 2 chains (i.e., skip the first 2 chains, return the next 2).
5. **Output**: The script must output a JSON file to `/home/user/failed_chains_page2.json`. The JSON should be a list of lists, where each inner list represents a single backup chain's `id`s from root to leaf. 

Example expected JSON format:
```json
[
  [12, 13, 14],
  [4, 5, 6]
]
```

Run your Python script to generate the JSON file.