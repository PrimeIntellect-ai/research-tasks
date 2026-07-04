You are a Database Reliability Engineer managing a complex backup strategy for a mission-critical NoSQL document database. Backups consist of a mix of full, incremental, and differential snapshots. Due to a recent failure, you need to automate the generation of an optimal restoration plan.

The backup metadata is stored as a collection of JSON documents representing the backup catalog. You need to perform cross-representation mapping: converting this document-oriented NoSQL metadata into a graph representation to efficiently compute dependencies and shortest paths, and then map the result back into a sequential execution pipeline.

I have placed the backup metadata at `/home/user/backups_metadata.json`.
Each document in the JSON array has the following schema:
- `backup_id` (string): Unique identifier for the backup.
- `type` (string): One of `full`, `incremental`, or `differential`.
- `timestamp` (integer): Epoch timestamp of when the backup was taken.
- `status` (string): Either `ok` or `corrupted`.
- `file` (string): The storage path of the backup file.
- `parent_id` (string or null): The `backup_id` of the backup this one depends on (for incremental/differential).

Your task is to write a Python script (you can name it `/home/user/planner.py`) that processes this data to find the optimal restoration chain to reach a specific target state. 

The requirements for the optimal chain are:
1. It must start with a `full` backup.
2. It must only contain backups with `status: "ok"`. If a backup in a chain is corrupted, no downstream backups depending on it can be used.
3. It must reach the highest possible `timestamp` that is **less than or equal to** the target timestamp of `1600003500`.
4. If there are multiple valid backup chains that reach this exact highest possible timestamp, you must choose the chain with the **fewest number of backup files** (shortest path) to minimize restoration time.
5. The output must be saved to `/home/user/restore_plan.json` as a JSON array of strings containing the exact `file` values in the order they must be restored.

You may use standard Python libraries or install third-party libraries like `networkx` using pip if you wish to materialize and project the graph.

Run your script to generate the `/home/user/restore_plan.json` file.