You are a Database Reliability Engineer. Our database backup system uses a chain of incremental backups. Each incremental backup depends on a specific parent backup, tracing all the way back to a full base backup (which has no parent). 

We recently exported the backup catalog metadata to a CSV file located at `/home/user/backup_metadata.csv`. The CSV has the following columns:
`backup_id,parent_backup_id,size_mb,status`
*A `parent_backup_id` of `NONE` indicates a full base backup.*

Your task is to write a purely Bash-based script (using standard CLI tools like `awk`, `grep`, `sed`, `jq`, etc., but no Python, Perl, or external scripting languages) to compute the restoration path.

1. Create a script at `/home/user/build_restore.sh` that takes a single argument: the target `backup_id`.
2. The script must trace the dependency graph from the target backup up to the root (the base backup where `parent_backup_id` is `NONE`).
3. As it traverses the hierarchy, it must sum the `size_mb` of all backups in the chain.
4. If every backup in the chain (including the target and the base) has a status of `SUCCESS`, the script should output a JSON object representing the valid restoration plan.
5. If *any* backup in the lineage has a status other than `SUCCESS`, or if a parent is missing from the CSV (broken chain), it must output an error JSON.

**Output Format Requirements:**
If the chain is valid and successful, print exactly this JSON to standard output:
```json
{
  "target": "<target_backup_id>",
  "valid": true,
  "chain": ["<base_backup_id>", "<next_incremental>", ..., "<target_backup_id>"],
  "total_size_mb": <integer_sum_of_sizes>
}
```
*Note: The `chain` array must be ordered from the base backup first, to the target backup last.*

If the chain is invalid (contains a failed backup or missing parent), print exactly this JSON to standard output:
```json
{
  "target": "<target_backup_id>",
  "valid": false
}
```

Once your script is complete, use it to generate two restoration plans:
1. Run `./build_restore.sh bkp_007` and redirect the output to `/home/user/restore_plan_1.json`.
2. Run `./build_restore.sh bkp_009` and redirect the output to `/home/user/restore_plan_2.json`.