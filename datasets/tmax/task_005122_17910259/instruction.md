You are a data analyst tasked with processing graph data exported from an old system. The data is stored in CSV files located in `/home/user/graph_data/`. 

The data represents directed edges in a graph (e.g., communication from one node to another). However, the system that exported this data had a corrupted index, resulting in stale and corrupted rows being mixed into the exports.

Your objectives:
1. **Reverse Engineer and Filter:** Inspect the CSV files to understand the schema. You must filter out any invalid edges. An edge is only valid if its `record_status` is exactly `ACTIVE` and its `timestamp` is greater than or equal to `1700000000`.
2. **Graph Analytics (Centrality):** For the filtered, valid graph, calculate the **Degree Centrality** of every node. In this directed graph context, a node's Degree Centrality is defined as the sum of its in-degree (number of times it appears as a destination) and its out-degree (number of times it appears as a source).
3. **Aggregation and Pagination:** Find the top 3 most central nodes. Sort the results by Degree Centrality in descending order. If there is a tie, resolve it by sorting the `node_id` in ascending alphabetical order.
4. **Schema Validation & Output:** Write a Bash script at `/home/user/analyze_graph.sh` that performs this entire process and outputs the final result to `/home/user/top_nodes.json`. The output must perfectly match this JSON schema format:
```json
[
  {
    "node_id": "NODE_NAME",
    "centrality": 99
  },
  ...
]
```

Constraints:
- You must use Bash and standard Linux command-line utilities (like `awk`, `sort`, `jq`, `grep`) to perform the data processing and aggregation. Do not use external scripting languages like Python or Node.js.
- Ensure your output JSON contains exactly 3 objects (the top 3 nodes).
- Make sure to execute your script so that `/home/user/top_nodes.json` is generated for verification.