You are a data analyst tasked with processing a Bill of Materials (BOM) represented as a directed acyclic graph.

You have been provided with two CSV files in your home directory:
1. `/home/user/nodes.csv`: Contains the nodes of the graph. Columns: `node_id`, `base_cost`, `node_type`.
2. `/home/user/edges.csv`: Contains the parent-child relationships and quantities. Columns: `parent_id`, `child_id`, `multiplier`.

Your objective is to write a Python script that analyzes this data to compute two specific metrics for the final product with the `node_id` of `PRODUCT_A`:

1. **Total Accumulated Cost**: The total cost to build `PRODUCT_A`. The cost of a node is defined recursively as its own `base_cost` plus the sum of `(cost_of_child * multiplier)` for all of its immediate children. 
2. **Maximum Raw Material Depth**: The longest path (measured in number of edges) from `PRODUCT_A` to any node of type `RAW_MATERIAL`.

You must write a Python script to perform this recursive traversal, materialization, and aggregation. 

Once calculated, your script must output exactly these two metrics into a JSON file located at `/home/user/bom_summary.json` with the following format:
```json
{
  "total_cost": 142.0,
  "max_depth": 3
}
```
(Note: The numbers above are examples, you need to calculate the actual values based on the CSV data).

Ensure your script runs successfully and writes the file accurately.