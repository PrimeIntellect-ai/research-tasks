You are a data analyst tasked with processing graph data using standard Bash tools (like `awk`, `grep`, `sort`, `join`). 

You have been provided with two CSV files (which you should assume exist, but you can create sample versions to test your code):
1. `/home/user/nodes.csv`: Contains information about nodes in a transaction network. Schema: `node_id,status`
2. `/home/user/edges.csv`: Contains directed transactions between nodes. Schema: `source_node,target_node,cost`

Your task consists of three phases:

**Phase 1: Graph Projection and Filtering**
Generate a projected graph file at `/home/user/projected_edges.csv`.
- Filter `edges.csv` to only include edges where BOTH the `source_node` and `target_node` have a status of `active` in `nodes.csv`.
- Exclude any edges where the `cost` is less than or equal to 0.
- The output schema must be strictly: `source_node,target_node,cost` (comma-separated, no headers).
- Sort the output lexicographically by `source_node`, then `target_node`.

**Phase 2: Graph Traversal (Shortest Path)**
Write a pure Bash/AWK script at `/home/user/find_path.sh` that reads `/home/user/projected_edges.csv` and finds the shortest path (by the minimum number of hops/edges, ignoring cost) from the node `START` to the node `END`.
- Assume the graph is small enough to fit in memory.
- If multiple paths have the same minimum number of hops, pick the one that is lexicographically first based on the sequence of nodes.

**Phase 3: Output Schema Validation**
Execute your script and save the resulting path to `/home/user/shortest_path.csv`.
- The output must strictly follow the schema: `step_index,node_id`
- `step_index` starts at 0 for the `START` node.
- Example valid output:
0,START
1,NODE_A
2,END

Ensure your final scripts and output files are placed exactly at the specified paths. Do not use Python, Perl, or any non-standard Unix utilities; rely only on standard Bash built-ins and GNU coreutils (awk, sed, grep, join, sort, etc.).