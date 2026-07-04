You are a Database Reliability Engineer (DBRE) responsible for managing backups across a complex architecture of database clusters, nodes, and storage volumes.

Your infrastructure metadata is stored in a local SQLite database acting as a knowledge graph. The database is located at `/home/user/infra_graph.db`. 

It has the following schema:
```sql
CREATE TABLE nodes (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL -- Can be 'cluster', 'node', or 'volume'
);

CREATE TABLE edges (
    source_id INTEGER,
    target_id INTEGER,
    relation TEXT, -- e.g., 'contains', 'mounts'
    FOREIGN KEY(source_id) REFERENCES nodes(id),
    FOREIGN KEY(target_id) REFERENCES nodes(id)
);
```

Your task is to write a Bash script `/home/user/generate_backup_plan.sh` that takes a cluster name as its first positional argument. 

The script must:
1. Use a parameterized SQLite recursive CTE (Common Table Expression) to traverse the knowledge graph starting from the given cluster name.
2. Find all `volume` nodes that are downstream descendants of the specified cluster (i.e., a cluster contains nodes, and nodes mount volumes).
3. Chain the output of this query into a text processing pipeline to format the backup commands.
4. Output the results alphabetically by volume name to a file named `/home/user/backup_plan.txt`. 

For each volume found, the script should append the following exact line to `/home/user/backup_plan.txt`:
`[BACKUP-EXEC] Starting snapshot for volume: <volume_name>`

For example, if the script is run as `./generate_backup_plan.sh analytics-cluster`, and that cluster ultimately mounts `vol-101` and `vol-202`, the `/home/user/backup_plan.txt` file should contain:
```text
[BACKUP-EXEC] Starting snapshot for volume: vol-101
[BACKUP-EXEC] Starting snapshot for volume: vol-202
```

Requirements:
- The script must be executable (`chmod +x`).
- Do not use temporary files for the query output; use Bash pipes to chain the SQLite output directly into your formatting logic.
- Ensure the output file `/home/user/backup_plan.txt` is overwritten (not just appended to) at the start of each script execution.
- Only include nodes of type `volume`.

Once you have written and tested the script, run it with the argument `prod-db-cluster` so the final `/home/user/backup_plan.txt` is generated for verification.