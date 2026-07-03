You are a Database Reliability Engineer handling a critical incident. We need to restore a specific backup, `auth_db_snapshot_2023`, from its current storage node to our recovery cluster node, `ap-northeast-1`. 

Because of current network routing constraints, backups cannot always be transferred directly. You must calculate the optimal transfer path through our global storage network.

Here is what you have:
1. A SQLite database at `/home/user/backups.db` containing a table `backups` with columns `id`, `name`, `size_mb`, and `current_node`.
2. A network topology file at `/home/user/network_topology.json` containing the available links between storage nodes. Each link has a `source`, `target`, `latency_ms`, and `bandwidth_mbps` (megabytes per second). Links are strictly unidirectional.
3. A JSON schema file at `/home/user/schema.json` that defines the exact format required for our automated transfer system.

Your task:
Write a Python script that:
1. Queries `/home/user/backups.db` to find the `size_mb` and `current_node` of `auth_db_snapshot_2023`.
2. Reads `/home/user/network_topology.json` and models it as a graph.
3. Computes the optimal (shortest) path from the backup's `current_node` to `ap-northeast-1`. The weight of each edge for this calculation must be the total transfer time in milliseconds, calculated as: `latency_ms + (size_mb / bandwidth_mbps) * 1000`.
4. Aggregates the route into a final JSON file saved at `/home/user/transfer_plan.json`.
5. Validates the resulting JSON against the schema in `/home/user/schema.json` (you may use the `jsonschema` library). 

The generated `/home/user/transfer_plan.json` must strictly pass the provided JSON schema. Ensure your script outputs the file correctly formatted.