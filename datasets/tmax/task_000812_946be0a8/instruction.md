You are a data engineer building an ETL pipeline to process financial process dependencies. The system frequently encounters "deadlocks" in the form of circular dependencies (cycles) between process transactions. Your task is to materialize a clean Directed Acyclic Graph (DAG) by programmatically breaking these cycles.

You have been provided a dataset at `/home/user/transactions.csv` with the following headers:
`tx_id,from_node,to_node,timestamp,weight`

Each row represents a directed edge (a dependency) from `from_node` to `to_node`. Your goal is to write a Python script that reads this file and constructs a DAG using the following strict deterministic rules to resolve any cycles:

1. Read all edges from the CSV.
2. Sort the edges to determine the order of evaluation. Sort them primarily by `weight` in DESCENDING order. If weights are tied, sort by `timestamp` in DESCENDING order. If both are tied, sort by `tx_id` ALPHABETICALLY (A-Z).
3. Initialize an empty Directed Graph (you may use the `networkx` library).
4. Iterate through your sorted list of edges. For each edge, attempt to add it to the graph.
5. If adding the edge creates a cycle (meaning the graph is no longer a valid DAG), immediately remove/discard that edge and continue to the next one.
6. Once all edges are processed, calculate the sum of the `weight` values for all the accepted edges.

Finally, output the result of your pipeline to a JSON file located at `/home/user/materialized_pipeline.json`. The JSON file must have exactly the following structure:
```json
{
  "total_weight": 1480,
  "accepted_tx_ids": ["TX01", "TX02", "TX03"]
}
```
*Note: `accepted_tx_ids` should be a alphabetically sorted list of the `tx_id` strings of the edges that successfully made it into the final DAG.*

You can use standard Linux tools, Python 3, and `pip` to install any necessary libraries (like `networkx` or `pandas`).