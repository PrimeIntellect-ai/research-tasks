You are a Database Reliability Engineer (DBRE) responsible for managing disaster recovery backups across a globally distributed storage network. 

We have an SQLite database located at `/home/user/backup_network.db` that contains metadata about our backups and the network topology. The database has two tables:

1. `backups`: Contains the history of backups taken at various storage nodes.
   - `id` (TEXT): Unique identifier for the backup.
   - `node_id` (INTEGER): The ID of the storage node where the backup resides.
   - `timestamp` (INTEGER): UNIX timestamp of the backup.
   - `size_bytes` (INTEGER): Size of the backup.

2. `network`: Represents the directed network links between storage nodes and the latency/cost to transfer data.
   - `source_node` (INTEGER)
   - `dest_node` (INTEGER)
   - `transfer_cost` (INTEGER): The cost of transferring data along this link.

Your task is to write a C++ program at `/home/user/process_backups.cpp` that performs the following:

1. Connects to `/home/user/backup_network.db`.
2. Uses an SQL query with a **Window Function** to identify the *latest* backup (highest timestamp) for each `node_id` (excluding node `0`, which is the central archive).
3. Queries the `network` table to build an in-memory graph.
4. Uses a graph traversal algorithm (e.g., Dijkstra's algorithm) to compute the shortest path (minimum `transfer_cost`) from each node to the central archive node (`node_id = 0`).
5. Generates a resulting CSV file at `/home/user/backup_plan.csv` detailing the replication plan. 

The output CSV must contain a header and be formatted exactly as follows:
```csv
node_id,backup_id,size_bytes,path_cost
```
The rows should be ordered by `node_id` in ascending order. If a node cannot reach node `0`, omit it from the output.

Requirements:
- The system has `sqlite3` and `libsqlite3-dev` installed.
- You must compile your C++ program using: `g++ -std=c++17 /home/user/process_backups.cpp -lsqlite3 -o /home/user/process_backups`
- Execute your compiled program to generate the `/home/user/backup_plan.csv` file.