You are a Database Reliability Engineer (DBRE) managing a complex backup and replication topology. Your infrastructure's recovery pathways are defined as a graph where nodes are database instances or storage archives, and edges are the replication/restoration links between them. 

During a simulated disaster recovery drill, you need to find the optimal restoration path from our deep cold storage to the primary production database.

You have been provided with two CSV files in your home directory:
1. `/home/user/nodes.csv` - Contains the backup nodes. Format: `id,type,size_gb`
2. `/home/user/edges.csv` - Contains the directed restoration links. Format: `source,target,restore_time_min`

Your task is to write a Go program (`/home/user/recovery.go`) using only the standard library that:
1. Parses the CSV files to build an in-memory graph.
2. Performs a graph traversal (e.g., Dijkstra's algorithm) to find the shortest restoration path from `s3_deep_archive` to `prod_main_db` optimized for the lowest total `restore_time_min`.
3. Calculates the cumulative `size_gb` of all nodes along this optimal path (an analytical aggregation acting similarly to a rolling sum window function).
4. Writes the result to `/home/user/recovery_plan.txt` in the exact format shown below.

Expected format for `/home/user/recovery_plan.txt`:
```
Path: nodeA -> nodeB -> nodeC
Total Time: X min
Cumulative Size: Y GB
```

Ensure your Go program is completely self-contained, compiles successfully, and produces the correct output file when run via `go run /home/user/recovery.go`. Do not use any third-party Go packages.