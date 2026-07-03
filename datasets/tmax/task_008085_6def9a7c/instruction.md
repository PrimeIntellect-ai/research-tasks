You are a data engineer tasked with building an ETL pipeline step that projects and materializes graph data.

You have been provided with a raw edge list in a CSV file located at `/home/user/raw_graph.csv`. 
The CSV has the following header: `src,dst,weight`. 
It represents a directed graph where edges have integer weights.

Your task is to write a Go program at `/home/user/graph_etl.go` that reads this CSV file and materializes a specific projection of the graph into a JSON file at `/home/user/materialized_graph.json`.

The ETL projection logic must strictly adhere to the following rules:
1. **Filtering (Query Optimization):** Only consider edges where the `weight` is greater than or equal to `5`. Ignore any edges with a weight less than 5.
2. **Graph Materialization:** Convert the filtered edge list into an adjacency list format representing the outgoing edges for *every* node that appears in the original dataset (either as a `src` or `dst`, regardless of whether their specific edges were filtered out).
3. **Output Schema:** The output must be a valid JSON array of objects. Each object must have exactly the following schema:
   - `node` (string): The name of the node.
   - `neighbors` (array of strings): An alphabetically sorted list of destination nodes for the outgoing valid edges from this node. If a node has no outgoing valid edges, this must be an empty array `[]`.
   - `total_weight` (integer): The sum of the weights of the valid outgoing edges. If there are no valid outgoing edges, this must be `0`.
4. **Ordering:** The final JSON array must be sorted alphabetically by the `node` field.

Ensure your Go code compiles and runs successfully. The automated test will run `go run /home/user/graph_etl.go` and then strictly verify the schema and contents of `/home/user/materialized_graph.json`.