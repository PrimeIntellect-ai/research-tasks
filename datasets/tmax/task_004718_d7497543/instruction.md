You are a Database Reliability Engineer managing backups across multiple distributed clusters. You need to migrate from a legacy, slow binary tool to a custom Python solution to compute optimal backup restoration paths.

We have a stripped legacy binary at `/app/oracle_planner` that calculates the cheapest backup restoration sequence. It is treated as a black-box oracle. It takes two arguments: a source backup ID and a target backup ID, and prints the optimal restoration path as a comma-separated list of IDs (or "UNREACHABLE" if no path exists).

The backup environment is modeled across two data stores:
1. A SQLite database at `/home/user/db_inventory.db` containing:
   - `restore_points`: (id INTEGER, snapshot_name TEXT, environment TEXT)
   - `datacenter_map`: (environment TEXT, datacenter_name TEXT, cost_multiplier REAL)
2. A directory of JSON documents at `/home/user/deps/` containing files like `1.json`, `2.json`, etc. Each JSON file is named after a source restore point ID and contains its directed outgoing transitions. Format: `[{"target_id": 5, "base_cost": 10}, ...]`.

The true cost of transitioning from backup A to backup B is the `base_cost` (from A's JSON file) multiplied by the `cost_multiplier` of backup A's environment (from the SQLite DB).

You have a starter script `/home/user/query_builder.py` that is meant to extract the `cost_multiplier` for every `restore_point`. However, the SQL query inside it is returning massively duplicated, incorrect results due to an implicit cross join.

Your tasks:
1. Identify and fix the cross join bug in the SQL query logic (whether in the script or by writing your own query).
2. Write a Python script at `/home/user/restore_planner.py` that computes the shortest path between any two restore point IDs.
3. Your script must be executable as `python3 /home/user/restore_planner.py <source_id> <target_id>` and output exactly the same comma-separated string as `/app/oracle_planner`.
4. Ensure your script handles cross-representation mapping (SQLite + JSON) correctly to build the graph and calculate the weighted edges before computing the shortest path.

Do not hardcode outputs. An automated verifier will randomly fuzz your script against the legacy oracle with hundreds of different source and target pairs to ensure bit-exact equivalence.