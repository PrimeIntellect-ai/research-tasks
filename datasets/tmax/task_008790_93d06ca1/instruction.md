You are a data analyst working with a communication network dataset. You have been provided with a CSV file `/home/user/network.csv` containing network edges with the header `source,target,weight`.

Your task is to process this data using Python and SQLite to perform database optimization and graph analytics. 

Please perform the following steps:

1. **Database Setup & Indexing**:
   Write and execute a Python script that creates an SQLite database at `/home/user/network.db`.
   Load the data from `/home/user/network.csv` into a table named `edges` (columns: `source` INTEGER, `target` INTEGER, `weight` REAL).
   Design and create an index (or indexes) on the `edges` table specifically optimized for querying all outgoing edges from a given `source` node.

2. **Query Plan Extraction**:
   Extract the SQLite execution plan for the query: `SELECT target, weight FROM edges WHERE source = 5;`
   Save the exact text output of `EXPLAIN QUERY PLAN SELECT target, weight FROM edges WHERE source = 5;` to `/home/user/plan.txt`. (It should show that your index is being used).

3. **Graph Analytics**:
   Write a Python script (using the `networkx` library) to read the edges from your SQLite database and build a directed graph. Using this graph:
   - Compute the **Betweenness Centrality** for all nodes (use the default `networkx` parameters, do not use weights for this metric). Save the top 3 nodes with the highest centrality scores to `/home/user/centrality.csv` in the format `node,score` (round the score to exactly 4 decimal places).
   - Compute the shortest path (using the `weight` column as the edge weight) from node `1` to node `50`. Save the sequence of nodes in the path as a comma-separated list (e.g., `1,4,10,50`) to `/home/user/path.txt`.

Ensure all output files (`/home/user/network.db`, `/home/user/plan.txt`, `/home/user/centrality.csv`, `/home/user/path.txt`) are generated correctly. You may install any necessary Python packages (like `pandas`, `networkx`) using pip.