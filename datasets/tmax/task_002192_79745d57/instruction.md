You are a Database Reliability Engineer investigating backup chain bloat. Our backup metadata is stored in a SQLite database located at `/home/user/backups.db`.

The database contains a table `backups` with the following schema:
`id TEXT PRIMARY KEY`
`parent_id TEXT` (References the previous backup in the incremental chain; NULL for full backups)
`size_bytes INTEGER`
`backup_time DATETIME`

Your task is to write a Go program at `/home/user/analyze_backups.go` that performs the following actions:

1. **Index Creation**: Execute a SQL command within your Go program to create an index named `idx_backups_parent` on the `parent_id` column to optimize hierarchical traversal.
2. **Graph Projection & Analytical Aggregation**: Use a single SQL query with a Recursive Common Table Expression (CTE) to traverse the backup chain starting from the full backup with `id = 'full_alpha'`. Along with the traversal, use a Window Function to calculate the `running_total_bytes` (the cumulative sum of `size_bytes` from the start of the chain up to each node, ordered by the recursive depth).
3. **Output Schema Validation**: The Go program must write the results of this query to `/home/user/chain_summary.json`. The output must be a strictly formatted JSON array of objects, with each object matching this schema exactly:
```json
[
  {
    "backup_id": "full_alpha",
    "depth": 0,
    "size_bytes": 50000,
    "running_total_bytes": 50000
  },
  ...
]
```

Requirements:
- Ensure you initialize a Go module and fetch the SQLite driver (`github.com/mattn/go-sqlite3`).
- Run your Go program so the database is indexed and the JSON file is generated.
- The depth should start at 0 for 'full_alpha' and increment by 1 for each subsequent incremental backup.