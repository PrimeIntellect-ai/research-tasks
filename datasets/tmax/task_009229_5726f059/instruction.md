You are a Database Reliability Engineer (DBRE) responding to a potential security incident. A database server (`db-srv-042`) has been compromised. You need to trace all backup storage nodes that might have been affected by lateral movement through our backup job replication network. 

Our infrastructure metadata is currently fragmented across two different formats in the directory `/home/user/backup_metadata`:
1. `/home/user/backup_metadata/servers.json`: A document-based export containing database servers and the backup jobs configured on them. Each job specifies its `primary_storage` node.
2. `/home/user/backup_metadata/storage_relations.csv`: A relational CSV export mapping `source_storage` nodes to their `replica_storage` nodes.

Your task is to:
1. Write a C++ program at `/home/user/analyze_backups.cpp` that reverse-engineers the data models from these fragmented files and unifies them into a single directed graph. 
2. The graph edges should represent the flow of backups: Database Server -> Backup Job -> Primary Storage Node -> Replica Storage Node. All edges have a weight of 1.
3. Compute the shortest path distance from the compromised server `db-srv-042` to all reachable storage nodes (both primary and replica).
4. Output the results to a file at `/home/user/audit_list.txt`.

The format of `/home/user/audit_list.txt` must be exactly:
`[StorageNodeName]: [Distance]`
One per line, sorted primarily by distance (ascending) and secondarily by storage node name (alphabetical). Only include storage nodes (do not include jobs or DB servers in the output).

Notes:
- You may install any necessary C++ packages via `apt` (e.g., `nlohmann-json3-dev` for JSON parsing).
- Compile with `-std=c++17` or higher.
- Ensure your program runs and generates the exact output file specified.