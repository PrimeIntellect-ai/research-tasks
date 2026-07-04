You are a Database Reliability Engineer (DBRE) tasked with auditing the integrity and disk-space footprint of your database backup chains. 

You have a CSV file located at `/home/user/backups.csv` containing metadata about recent backups. The columns are: `id,parent_id,type,size_bytes,status`.

- `id`: Unique string identifier for the backup.
- `parent_id`: The `id` of the preceding backup this backup depends on (empty if it's a `FULL` backup).
- `type`: Either `FULL` or `INCREMENTAL`.
- `size_bytes`: Integer representing the size of the backup file itself.
- `status`: Either `OK` or `CORRUPT`.

A backup chain forms a directed hierarchy (a tree) starting from a `FULL` backup down through its `INCREMENTAL` descendants. 
A "restore point" is valid ONLY IF the backup itself is `status=OK` AND all of its ancestors up to the `FULL` backup are also `status=OK`. If any ancestor is `CORRUPT`, the backup and all its descendants are invalid restore points.

The "materialized size" of a valid restore point is the sum of its own `size_bytes` and the `size_bytes` of ALL its ancestors.

**Your Task:**
1. Write a Go program at `/home/user/analyze.go` using ONLY the Go standard library.
2. The program must read `/home/user/backups.csv`, perform a hierarchical projection of the backup graph, and calculate the materialized size of all **valid** restore points.
3. The program must output the results to a JSON file at `/home/user/valid_restore_points.json`.

**Output Format Requirements:**
The output file `/home/user/valid_restore_points.json` must contain a JSON array of objects, sorted by `id` in ascending alphabetical order. Each object must have exactly two keys:
- `"id"` (string)
- `"materialized_size"` (integer)

Example expected format:
```json
[
  {"id": "A1", "materialized_size": 1000},
  {"id": "A2", "materialized_size": 1100}
]
```

Run your Go program to generate the JSON file. Let me know when you are finished.