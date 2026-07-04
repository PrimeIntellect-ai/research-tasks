You are a database administrator tasked with optimizing complex NoSQL aggregation pipelines. The execution plan of a massively chained aggregation query has been dumped as a directed graph in JSON format at `/home/user/query_plan.json`.

The JSON file contains two arrays: `nodes` (representing pipeline operators, with their `id`, `type`, and execution `cost`) and `edges` (representing data flow, with `source` and `target` node IDs).

Your task is to identify the most heavily reused operator type and calculate its total cost impact across the entire pipeline. To do this, you must exclusively use Bash commands (like `jq`, `awk`, `sort`, etc.):

1. Determine the out-degree for each node (the number of times a node's `id` appears as a `source` in the `edges` array).
2. Identify the node `id` with the highest out-degree. If there is a tie, select the one that comes first alphabetically by `id`.
3. Find the `type` of this specific node. Let's call this the "Bottleneck Type".
4. Calculate the sum of the `cost` for **all** nodes in the graph that have this exact same `type`.
5. Write the final result to `/home/user/optimization_report.txt` in the exact following format:
   `Bottleneck_Type: <type> | Total_Cost: <sum>`

Ensure you output only that exact string to the file, with a single trailing newline.