You are a data engineer building an ETL pipeline to analyze transaction networks. 

You need to write a Python script at `/home/user/etl_pipeline.py` that performs graph analytics, projects a materialized subgraph, and validates the output schema.

Here are the requirements for the pipeline:
1. **Input Data**: Read a CSV file located at `/home/user/data/edges.csv`. The file has three columns: `src`, `dst`, and `weight` (representing directed edges from `src` to `dst`).
2. **Graph Construction**: Build a Directed Graph using the `networkx` library. Use the `weight` column as edge weights.
3. **Graph Analytics**:
   - Compute the PageRank for each node using `networkx.pagerank` with default parameters (alpha=0.85, weight='weight').
   - Determine the weakly connected components of the graph. For each node, calculate the size of the weakly connected component it belongs to (`component_size`).
4. **Subgraph Projection**: Filter the graph to retain only nodes that belong to a weakly connected component of size `>= 3`.
5. **Output Materialization**: Write the metrics for the retained nodes to `/home/user/output/nodes.jsonl` in JSON Lines format.
6. **Schema Validation**: Each JSON object in the output must strictly match the following schema:
   - `node_id`: string (the name of the node)
   - `pagerank`: float
   - `component_size`: integer
7. **Sorting**: Sort the records alphabetically by `node_id` before writing them to the file.

Before running your script, create the output directory `/home/user/output/` if it does not exist.
You may install required Python packages (like `networkx`) using `pip`.