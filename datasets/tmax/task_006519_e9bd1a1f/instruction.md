You are a Database Reliability Engineer managing cross-region backups for a distributed database. Backups must be replicated between various data centers (nodes) across a network with varying latencies.

We have a C++ program located in `/home/user/backup_tool` designed to calculate the optimal backup transfer paths and analyze the network topology. However, the current code has a critical logic flaw: instead of traversing the network graph, it loops over all jobs and all edges simultaneously (acting as an implicit cross join) and wrongly sums up all network latencies, producing wildly inaccurate estimates.

Your task is to fix this tool by implementing proper graph algorithms and producing the correct reports.

**Setup Instructions:**
The workspace `/home/user/backup_tool` contains:
- `edges.csv` (format: `source_node,target_node,latency` - undirected edges)
- `jobs.csv` (format: `job_id,source_node,target_node`)
- `router.cpp` (The buggy codebase with empty/broken function stubs)
- `Makefile` 

**Requirements:**
1. Fix `router.cpp` to correctly build an adjacency list representing the network. The graph is undirected.
2. Implement Dijkstra's algorithm to find the shortest path (minimum latency) for each backup job listed in `jobs.csv`.
3. Implement a graph analytics function to calculate the **degree centrality** of each node (the number of direct connections it has).
4. Build the C++ program (using the provided `Makefile` or just running `make`).
5. Run the tool to generate two output reports:
   - `/home/user/top_jobs.csv`: Process all jobs, sort them by minimum latency in **descending** order. In case of a tie in latency, sort alphabetically by `job_id` ascending. Output only the top 3 jobs. Format: `job_id,latency`.
   - `/home/user/top_hubs.csv`: Process all nodes, sort them by degree centrality in **descending** order. In case of a tie, sort alphabetically by `node_id` ascending. Output only the top 3 nodes. Format: `node_id,degree`.

Both output files must include headers (`job_id,latency` and `node_id,degree` respectively) and be strictly comma-separated. Do not use external libraries beyond the C++ standard library.