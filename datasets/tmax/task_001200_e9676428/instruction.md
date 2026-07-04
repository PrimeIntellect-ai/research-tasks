You are a data analyst working with a network dataset. You have been provided with a raw CSV file containing edge list data from a network. Your task is to process this graph using Rust, calculate the weighted degree centrality of each node, and export a specific paginated view of the results.

Create a Rust project in `/home/user/graph_processor`. The project should read the input file located at `/home/user/edges.csv`.

The input CSV has the following columns (with a header row):
`source_node,target_node,timestamp,weight`

You need to implement the following logic in your Rust application:
1. **Schema Validation**: Parse the CSV file. If a row is malformed or if the `weight` column cannot be parsed as a positive integer (`u32`), you must silently ignore and skip that row.
2. **Graph Processing (Undirected)**: Calculate the "total weighted degree" for each node. The total weighted degree is the sum of the `weight` values of all valid edges connected to a node, treating the graph as undirected (i.e., an edge from A to B with weight 5 adds 5 to A's total and 5 to B's total). Self-loops (where source equals target) should add the weight to the node exactly once.
3. **Filtering**: Drop any nodes that have a total weighted degree of strictly less than `15`.
4. **Sorting**: Sort the remaining nodes by their total weighted degree in strictly **descending** order. If two nodes have the exact same total weighted degree, tie-break by sorting them by their node ID in **ascending** alphabetical order.
5. **Pagination**: Apply pagination to the sorted list. Skip the first 3 nodes (offset = 3) and take the next 4 nodes (limit = 4).
6. **Result Export**: Export the paginated subset to a JSON file at `/home/user/paginated_nodes.json`. 

The output must be a tightly formatted JSON array of objects with exactly this schema:
```json
[
  {
    "node_id": "NODE_NAME",
    "score": 123
  },
  ...
]
```

Ensure your project can be compiled and run with `cargo run --release`. Once your code writes the correct output to `/home/user/paginated_nodes.json`, you have completed the task.