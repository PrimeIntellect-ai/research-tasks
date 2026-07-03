You are a Database Reliability Engineer managing a large fleet of database backups. Your backup metadata is stored as NoSQL document logs in JSON Lines (JSONL) format. Incremental backups form a dependency graph, as each incremental backup refers to a `parent_id` (the previous backup snapshot).

You need to analyze these backups to identify critical bottlenecks in the backup dependency graph and rank storage consumption across different deployment regions.

There is an existing Rust project initialized at `/home/user/backup_analyzer/`. The metadata is provided at `/home/user/backups.jsonl`.

Each line in the JSONL file represents a backup snapshot and contains the following fields:
- `id` (String): The unique identifier of the backup snapshot.
- `parent_id` (String or null): The ID of the parent backup this incremental backup depends on.
- `size_bytes` (u64): The size of the backup in bytes.
- `region` (String): The cloud region where the backup is stored.

Your task is to write a Rust program inside the `/home/user/backup_analyzer/` project that reads `/home/user/backups.jsonl` and computes the following for each backup:
1. **Graph Out-degree (children_count):** The number of immediate children (incremental backups) that directly depend on this backup's `id` as their `parent_id`.
2. **Analytical Window Rank (region_rank):** The rank of the backup's `size_bytes` compared to other backups *within the same `region`*. The largest backup in a region gets rank 1, the second largest gets rank 2, and so on. If sizes are equal, rank them alphabetically by `id`.

The Rust program must output the results to a CSV file at `/home/user/critical_backups.csv`. 
The CSV must have the following header: `id,children_count,region_rank` and the rows must be sorted alphabetically by `id`.

Rules:
- You must write the solution in Rust in the provided `/home/user/backup_analyzer/` project.
- You can use standard libraries and the crates pre-configured in the project's `Cargo.toml` (`serde` and `serde_json`).
- Execute your code to produce the final `/home/user/critical_backups.csv`.