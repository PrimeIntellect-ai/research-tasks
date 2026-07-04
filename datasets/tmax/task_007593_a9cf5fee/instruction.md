You are a Database Reliability Engineer investigating a backup restoration system failure. A recent incident corrupted the index of our primary metadata database, causing it to return stale rows containing "ghost" backup segments that are actually corrupted. 

Your task is to calculate the fastest reliable restoration path by cross-referencing the relational database (which has the stale/corrupted index) with a source-of-truth document store. 

You must write a Rust program to perform this analysis. 

**Data Sources:**
1. **Relational Database**: `/home/user/backups.db` (SQLite3)
   - Table: `recovery_edges`
   - Schema: `src TEXT, dst TEXT, time_mins INTEGER`
   - This table represents a directed graph of backup states. An edge from `A` to `B` means backup state `B` can be restored from state `A` in `time_mins` minutes.
2. **Document Store**: `/home/user/node_status.json`
   - Format: A JSON array of objects, e.g., `[{"id": "NODE_A", "state": "valid"}, {"id": "NODE_B", "state": "corrupted"}]`.

**Requirements:**
1. Create a Rust Cargo project named `backup_router` in `/home/user/backup_router`.
2. Write a Rust program that reads both data sources.
3. Materialize a directed graph in memory, **filtering out** any edges where either the `src` or `dst` node has a state other than `"valid"` in the `node_status.json` file. Nodes not present in the JSON file should be considered invalid/corrupted.
4. Calculate the shortest path (minimum total `time_mins`) from the node `"DB_MAIN_FULL"` to the node `"RESTORE_COMPLETE"`.
5. The program must write the result to exactly `/home/user/restore_plan.txt` in the following format:
   ```
   Total Time: <X> mins
   Path: NODE1 -> NODE2 -> NODE3
   ```
   *(Where NODE1 is DB_MAIN_FULL and the final node is RESTORE_COMPLETE).*

Run your Rust program to generate the `/home/user/restore_plan.txt` file. You may use standard crates like `rusqlite`, `serde`, `serde_json`, and any graph/algorithm crates you prefer.