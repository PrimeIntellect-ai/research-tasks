You are a data analyst troubleshooting a network routing issue. You have received two data exports representing our server network: 

1. A CSV file located at `/home/user/network_edges.csv` containing network connections. The columns are `source_node, target_node, latency_ms, link_status`.
2. A JSON file located at `/home/user/node_metadata.json` containing server metadata.

Recently, several links went offline, but our legacy routing system (which reads from an older SQLite cache) is returning stale paths that include offline links. 

Your task is to write a Python script to compute the true shortest path (by `latency_ms`) from node `alpha` to node `omega` using only active links. 

Rules and Requirements:
- You must read the connections from `/home/user/network_edges.csv`.
- Ignore any edges where `link_status` is not exactly `active`.
- Compute the shortest path using the active edges. 
- Write the result to `/home/user/path_result.json`.

The output file `/home/user/path_result.json` MUST be strictly validated to match this exact JSON schema:
```json
{
  "path": ["alpha", "node1", "node2", "omega"],
  "total_latency_ms": 150
}
```
Replace the example array and integer with your computed shortest path sequence and total latency. Do not include any extra keys in the JSON file.