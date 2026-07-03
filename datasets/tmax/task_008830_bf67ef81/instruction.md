You are a data analyst investigating a corporate supply chain network. You have been provided with two CSV files representing a subset of a corporate knowledge graph:
1. `/home/user/nodes.csv`: Contains nodes in the network. Columns are `id`, `type`, and `name`.
2. `/home/user/edges.csv`: Contains relationships between nodes. Columns are `source`, `target`, and `relation`.

Your task is to write and execute a Python script that processes these CSV files to perform the following network analysis:
1. Construct an undirected graph from the nodes and edges.
2. Calculate the degree centrality for all nodes in the graph to identify the "hub" (the single node with the highest degree centrality). If there is a tie, pick the one with the lowest numeric ID.
3. Perform a pattern match to find all nodes of type `Supplier` that are directly connected (distance of exactly 1 edge) to this hub node.
4. Export the results to a JSON file located at `/home/user/top_suppliers.json`.

The output JSON file must contain a strictly formatted list of objects representing the matched suppliers, sorted in ascending order by their numeric `id`. Each object must contain the keys `id` (as an integer) and `name` (as a string).

Example output format for `/home/user/top_suppliers.json`:
```json
[
  {
    "id": 10,
    "name": "Example Supplier A"
  },
  {
    "id": 15,
    "name": "Example Supplier B"
  }
]
```

You may install any standard data science libraries (e.g., `networkx`, `pandas`) you need using pip.