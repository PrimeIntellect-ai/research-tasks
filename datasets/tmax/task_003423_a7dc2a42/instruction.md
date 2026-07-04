You are a database administrator and data engineer. We have a Python script that is supposed to extract a regional network topology from a SQLite database, perform graph analytics on it, and export the results. However, the script is currently broken, incredibly slow, and producing wildly incorrect results due to a bad SQL query (an implicit cross join) and improper query parameterization.

Your task is to fix and extend the script located at `/home/user/analyze_network.py`.

Here is what you need to do:

1.  **Fix the SQL Query**: 
    The script connects to `/home/user/network.db`. The database has two tables: 
    - `nodes (id TEXT PRIMARY KEY, region TEXT)`
    - `edges (source TEXT, target TEXT, weight REAL)`
    The current SQL query tries to fetch all edges where the `source` node belongs to a specific region. However, it uses an implicit cross join, returning duplicate/incorrect rows. Fix the SQL query to use proper `JOIN` syntax and correctly return only the edges `(source, target, weight)` where the `source` node's `region` matches the target region.

2.  **Secure Parameterization**:
    The script currently uses insecure string formatting to insert the region name into the SQL query. Change this to use standard SQLite parameterized queries (e.g., using `?`).

3.  **Graph Analytics**:
    The script needs to compute the **in-degree centrality** of the nodes in the extracted subgraph. 
    - Install `networkx` if it isn't already installed.
    - Build a Directed Graph (`nx.DiGraph`) using the extracted edges.
    - Calculate the in-degree centrality for all nodes in this subgraph.

4.  **Window Function SQL Export**:
    As a secondary request, we need a pure SQL query saved to `/home/user/ranking.sql`. Write a query that returns `source, target, weight, region, rank`, where `rank` is calculated using a Window Function (`RANK()`) that ranks edges by `weight` in descending order *within each region* (partitioned by region). Join the `nodes` and `edges` table properly based on `source = id`.

5.  **Output Export**:
    Modify `/home/user/analyze_network.py` so that when run with a region argument (e.g., `python3 /home/user/analyze_network.py us-east`), it calculates the in-degree centrality, sorts the nodes by their centrality score in descending order (and by node ID ascending in case of a tie), and exports the top 3 nodes to `/home/user/top_nodes.csv`.
    The CSV should have no header line, and the format should be exactly: `node_id,centrality_score` (round the centrality score to 4 decimal places).

Run your fixed script for the `us-east` region to generate the final `/home/user/top_nodes.csv` file. Ensure `/home/user/ranking.sql` is perfectly valid SQLite syntax.