You are a Database Reliability Engineer auditing backup integrity for a distributed database system. The backup system exports metadata for each backup job as a JSON document. These documents are stored in `/home/user/backup_metadata/`.

Your task is to write a Go program at `/home/user/audit.go` that reads all JSON files in this directory, processes the dependency graph of the backups, and aggregates statistics to identify the largest valid backup chain and any orphan backups.

Each JSON file has the following structure:
```json
{
  "id": "b1",
  "type": "full",         // or "incremental"
  "parent_id": null,      // ID of the parent backup, null for "full"
  "size_bytes": 1000,     // size of this specific backup
  "status": "success"     // or "failed"
}
```

### Validation Rules for Backup Chains:
1. **Valid Chain**: A valid chain starts with a `full` backup whose status is `"success"`.
2. **Valid Incremental**: An `incremental` backup is valid if and only if its status is `"success"`, its parent exists, and its parent is also valid (either a valid `full` backup or a valid `incremental` backup).
3. **Chain Size**: The size of a chain is the sum of `size_bytes` of the starting valid `full` backup and all of its valid `incremental` descendants. Failed backups or orphans are not counted in the chain size.
4. **Orphans**: An `incremental` backup is considered an "orphan" if it depends on a parent that is missing, a parent whose status is `"failed"`, or a parent that is itself an orphan. (Note: A `"failed"` backup is not considered an orphan unless its own parent meets the orphan criteria.)

### Requirements:
Write the Go program `/home/user/audit.go` to compute the following metrics across all backups:
- `total_valid_chains`: The total number of valid `full` backups.
- `largest_chain_start_id`: The `id` of the valid `full` backup that initiates the chain with the largest total size in bytes.
- `largest_chain_size`: The total size in bytes of that largest chain.
- `orphan_count`: The total number of orphan backups.

Your program must output these results as a single JSON object to `/home/user/report.json` with the exact keys mentioned above.

To complete the task:
1. Parse the JSON metadata files.
2. Build the dependency graph to traverse and validate the backup chains.
3. Perform the necessary cross-query aggregations to calculate chain sizes and identify orphans.
4. Run your Go program to produce `/home/user/report.json`.