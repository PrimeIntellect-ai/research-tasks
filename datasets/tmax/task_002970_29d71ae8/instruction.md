You are a Database Reliability Engineer. Our primary graph database cluster has crashed, and we are currently running in a degraded state using a partial backup distributed across multiple services. 

Unfortunately, the SQLite backup of our graph's edge list has a corrupted index that returns stale rows. You need to write a Python CLI tool that pieces together the true state of the graph by querying multiple services, filters out the stale data, and calculates specific graph analytics for our dashboard.

System Setup:
There are two services running locally, plus an SQLite database:
1. **SQLite Database** at `/app/data/graph_backup.db`. It contains a single table: `edges(source TEXT, target TEXT, weight REAL)`. Some of these edges are stale/corrupted.
2. **Redis** running on `localhost:6379`. It stores the true active status of nodes. A node is active if the Redis key `node:<id>:status` has the string value `"active"`. If the key is missing or has any other value, the node is permanently deleted.
3. **Flask Validation API** running on `localhost:8080`. You can `GET http://localhost:8080/api/validate?source=<id>&target=<id>`. It returns a JSON response: `{"valid": true}` or `{"valid": false}`.

An edge in the SQLite database is ONLY considered valid if ALL of the following are true:
- The `source` node is "active" in Redis.
- The `target` node is "active" in Redis.
- The Flask Validation API returns `{"valid": true}` for that specific source-target pair.

Your Task:
Write a Python script at `/home/user/graph_query.py` that takes a single positional CLI argument (a starting `node_id`).
The script must:
1. Identify all valid edges in the entire SQLite database by cross-referencing with Redis and the Flask API.
2. Construct a directed graph in memory using only the valid edges.
3. Calculate the number of strictly 1-hop neighbors (nodes reachable exactly 1 directed edge away from the starting node) and strictly 2-hop neighbors (nodes reachable exactly 2 directed edges away, which are NOT the starting node itself and NOT already counted as 1-hop neighbors).
4. Print exactly one line to standard output in this exact JSON format:
   `{"node": "<node_id>", "1_hop": <count>, "2_hop": <count>}`

Constraints & Requirements:
- You must use Python 3.
- Do not print any debug information to standard output (standard error is fine).
- Ensure your script is executable (`chmod +x /home/user/graph_query.py`) and begins with `#!/usr/bin/env python3`.
- The system will test your script against dozens of random node IDs to ensure it exactly matches the expected output.