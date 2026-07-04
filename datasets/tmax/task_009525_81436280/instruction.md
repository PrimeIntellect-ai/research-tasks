You are acting as a compliance officer auditing an internal network after a suspected data breach. We need to determine the most vulnerable (shortest) path an attacker could have taken from the public entry point (`ENTRY_PORTAL`) to our most sensitive database (`SECURE_VAULT`). 

We have exported the network access routing table from our NoSQL graph database into a JSON Lines format, located at `/home/user/access_logs.jsonl`. However, the index that produced this export is corrupted and returned "stale" routing rules alongside active ones. 

Your task:
1. Construct a shell pipeline to query and filter `/home/user/access_logs.jsonl`. You must extract only the edges where the `"status"` field is exactly `"active"`. You may format this filtered data however you choose (e.g., CSV, TSV) to feed into your C program.
2. Write a C program at `/home/user/audit_path.c` that reads the filtered, active-only network edges. Each edge has a `"source"`, `"target"`, and an integer `"weight"` (representing latency/difficulty).
3. The C program must compute the shortest path (lowest total weight) from `ENTRY_PORTAL` to `SECURE_VAULT` using graph traversal (e.g., Dijkstra's algorithm).
4. Run your pipeline and C program, then output the results to the following files:
   - `/home/user/shortest_path.txt` : The ordered list of node names in the shortest path, separated by commas (e.g., `ENTRY_PORTAL,NODE_1,NODE_2,SECURE_VAULT`).
   - `/home/user/total_weight.txt` : A single integer representing the total minimum weight of that path.

Constraints:
- You must use C as the primary language for the graph traversal calculation. Standard libraries only.
- Compile your C program to `/home/user/audit_path`.
- All shell commands and the C program execution should run cleanly in a standard Linux environment.