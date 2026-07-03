You are a data engineer building a lightweight ETL (Extract, Transform, Load) pipeline that works directly with a file-system-based NoSQL graph database. The database consists of numerous JSON files, each representing a node in a graph.

Your goal is to write a robust Bash script that traverses this graph, computes shortest paths, aggregates metrics, and filters results using standard Linux tools (like `bash`, `jq`, `sort`, `awk`, etc.).

**Data Specifications:**
- Directory: `/home/user/graph_db/nodes/`
- Each file is named `<node_id>.json` (e.g., `node_0.json`).
- File format:
  ```json
  {
    "id": "node_0",
    "weight": 42,
    "linked_nodes": ["node_5", "node_12"]
  }
  ```

**Task Requirements:**
Create an executable Bash script at `/home/user/etl_pipeline.sh` that takes two arguments:
1. `START_NODE` (e.g., `node_0`)
2. `END_NODE` (e.g., `node_49`)

When executed as `./etl_pipeline.sh <START_NODE> <END_NODE>`, your script must perform a graph traversal starting from `START_NODE` and generate a report at `/home/user/etl_report.txt` containing exactly three lines:

**Line 1: Shortest Path Hops**
Compute the shortest path from `START_NODE` to `END_NODE` in terms of the number of hops (edges). Output just the integer number of hops. If `START_NODE` is the same as `END_NODE`, the answer is 0. If `END_NODE` is completely unreachable from `START_NODE`, output `-1`.

**Line 2: Cross-Query Aggregation (Total Weight)**
Calculate the sum of the `weight` values for **all nodes that are reachable** from `START_NODE` (including `START_NODE` itself). Output this total sum as a single integer.

**Line 3: Result Sorting, Pagination, and Filtering**
Out of **all nodes reachable** from `START_NODE`, filter out any nodes that have a weight less than 20. For the remaining reachable nodes, sort them by `weight` in **descending** order. Paginate the result to get only the **top 3** node IDs. Output these 3 node IDs separated by a comma and a space (e.g., `node_8, node_41, node_3`). If multiple nodes have the same weight, sort them alphabetically by their `id` in ascending order. If fewer than 3 nodes remain after filtering, output the ones that do exist.

**Constraints & Rules:**
- The script must be written primarily in Bash.
- You may use standard Unix utilities (`jq`, `awk`, `sed`, `grep`, `sort`, etc.).
- Ensure your script correctly parameterizes commands to prevent injection or syntax errors if node names contain unusual characters (though in this dataset they are alphanumeric).
- The final state must have the output correctly written to `/home/user/etl_report.txt` after you manually execute your script with `./etl_pipeline.sh node_0 node_49`.