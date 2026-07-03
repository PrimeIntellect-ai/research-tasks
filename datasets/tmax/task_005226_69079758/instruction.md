You are a Database Reliability Engineer (DBRE) managing a backup infrastructure. 

We are experiencing an issue where backup routing sizes and paths are calculating incorrectly due to a combination of missing topology documentation and a corrupted SQLite index.

Your task is to write a Go program that correctly calculates the shortest path cost for backups to reach the `MASTER` node and retrieves the latest successful backup size, bypassing the corruption.

Here is the situation:
1. **Topology Recovery**: The network topology for our backup nodes is only available in an architectural diagram saved at `/app/topology.png`. You must use OCR (e.g., `tesseract`, which is installed) or visual inspection to extract the edges and weights between nodes. The image contains a list of connections in the format `NODE1-NODE2:WEIGHT` (edges are bidirectional).
2. **Database Querying**: Historical backup metadata is stored in an SQLite database at `/app/backups.db`. The table `backup_logs` has columns `id`, `node_id`, `timestamp`, `status`, and `size_bytes`. 
   - You need to find the `size_bytes` of the *most recent* backup where `status = 'SUCCESS'` for a given `node_id`. Use SQL window functions to determine the latest record.
   - **Warning**: The index `idx_backup_status` on the `status` column is corrupted and returns stale/ghost rows. You must ensure your query ignores or drops this index to get accurate results.
3. **Go Program**: Write a Go program at `/home/user/backup_route.go`.
   - The program must accept exactly one command-line argument: `node_id` (e.g., `go run backup_route.go NodeA`).
   - It must compute the shortest path (lowest total weight) from the given `node_id` to the `MASTER` node using the topology extracted from the image.
   - It must query the SQLite database for the latest successful backup size for that node.
   - It must print a strictly formatted JSON object to `stdout`: `{"node": "<node_id>", "latest_size": <size>, "route_cost": <cost>}`. If a node has no successful backups, `latest_size` should be `0`. If the node is `MASTER`, `route_cost` is `0`.

Ensure your Go program is highly robust, as it will be rigorously tested against multiple node IDs by an automated fuzzer comparing it to a verified oracle. Ensure all JSON keys strictly match the specification.