You are a database administrator tasked with optimizing network routing queries for a logistics company. The network topology data is stored in an undocumented SQLite database located at `/home/user/network.db`. 

Historically, the team used complex SQL recursive Common Table Expressions (CTEs) to find routing paths, but performance has degraded. Your goal is to reverse-engineer the database schema, extract the necessary graph data, and use Python to efficiently compute the optimal route.

Specifically, you need to:
1. Inspect `/home/user/network.db` to understand how network devices and their connections (edges) are represented, including the latency (weight) of each connection. Note that connections are strictly directional.
2. Write a Python script at `/home/user/optimize_route.py` that connects to this database, reads the topology, and computes the shortest path (the route with the lowest total latency) from the device with the hostname `gateway-alpha` to the device with the hostname `storage-omega`.
3. Export the resulting shortest path to a JSON file located at `/home/user/optimal_path.json`. The file must contain exactly one JSON array of strings representing the ordered sequence of hostnames in the optimal path, starting with `"gateway-alpha"` and ending with `"storage-omega"`.

Example of expected output format in `/home/user/optimal_path.json`:
`["gateway-alpha", "core-router-1", "storage-omega"]`

Ensure your Python script runs successfully and generates the exact JSON format required.