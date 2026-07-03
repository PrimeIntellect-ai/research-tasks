You are a database administrator tasked with optimizing and extracting analytics from an SQLite database that models a dependency graph. 

The database is located at `/home/user/dependency_graph.db`. 

We know the database contains two main tables (you will need to reverse-engineer their exact schema):
1. A table representing graph edges (source and target nodes).
2. A table representing node metrics (node ID, category, and a performance score).

Currently, retrieving ranked performance data for a specific subgraph is extremely slow. Your task is to:

1. **Optimize the Database**: Analyze the query plan for joining edges and metrics. Create an optimal composite index in the SQLite database that specifically speeds up grouping/windowing by `category` and sorting by `score` in descending order. Name this index `idx_category_score`.
2. **Write an Analytics Script**: Create a Python script at `/home/user/analyze_subgraph.py` that takes a single command-line argument: a `source_node` ID (integer).
3. **Query Requirements**: The script must securely use parameterized queries (no f-strings for the node ID) to find all *direct* target nodes connected to the given `source_node`. For these target nodes, use a SQL Window Function to calculate their `RANK()` within their respective `category` based on their `score` (highest score gets rank 1). 
4. **Output**: The script must output the result as a strictly formatted JSON array of dictionaries to stdout, ordered by `rank` ascending, then `node_id` ascending. Each dictionary should have the keys: `"node_id"`, `"category"`, `"score"`, and `"category_rank"`.
5. **Save Results**: Run your script for `source_node` = 100 and save the standard output to `/home/user/output_100.json`.

Ensure your Python script relies on `sqlite3` and executes efficiently.