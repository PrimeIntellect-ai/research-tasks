You are a Database Reliability Engineer managing the recovery of a legacy graph database. The database has crashed, and the only recoverable artifact is a raw CSV backup of its routing edges located at `/home/user/backup/edges.csv`. 

To design an optimal index strategy and schema for the new replacement database, you must identify the most heavily connected "hotspot" nodes. Creating targeted indexes on these high-traffic nodes will significantly improve our query performance upon restoration.

Your task is to write a C program that performs graph analytics on this backup and exports the results in a strict JSON schema.

Requirements:
1. Write a C program at `/home/user/analyze_graph.c`.
2. The program must read `/home/user/backup/edges.csv`. The CSV contains directed edges with no header, formatted as `source_id,target_id` (both are standard 32-bit integers).
3. Compute the **total degree centrality** (in-degree + out-degree) for every node present in the dataset.
4. Identify the top 3 nodes with the highest total degree. If there is a tie in degrees, resolve it by prioritizing the smaller `node_id`.
5. The C program must export these top 3 nodes to `/home/user/index_priority.json`.
6. The JSON output must strictly validate against this format (array of objects):
```json
[
  {"node_id": X, "degree": Y},
  {"node_id": X, "degree": Y},
  {"node_id": X, "degree": Y}
]
```
7. Compile and run your C program to generate the file. 

The resulting `/home/user/index_priority.json` file will be picked up by our automated schema migration tool. Ensure the formatting is exact and valid JSON.