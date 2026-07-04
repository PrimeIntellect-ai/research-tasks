We are migrating our data pipelines from a legacy graph processing system. The old system uses a proprietary ETL tool located at `/app/legacy_etl` (a stripped binary). 

Your task is to build a modern C++ replacement for the analytics portion of this pipeline.

Step 1: Environment Setup & Data Generation
Install any necessary C++ SQLite libraries. Then, run the legacy tool to generate the initial database:
`/app/legacy_etl /home/user/graph.db 5000`
This generates a SQLite database at `/home/user/graph.db` containing a table `edges(src INTEGER, dst INTEGER)`. 

Step 2: Database Repair
The legacy ETL tool has a known bug: it creates a corrupted index `idx_src` on the `edges` table, which causes subsequent queries to return "stale" or ghost edges that shouldn't exist. You must repair `/home/user/graph.db` so that standard SQL queries return the correct, uncorrupted graph structure.

Step 3: Graph Extraction & Analytics (C++)
Write a C++ program at `/home/user/graph_analyzer.cpp` that does the following:
1. Connects to `/home/user/graph.db`.
2. Uses a **Recursive Common Table Expression (CTE)** to find the active subgraph: all nodes reachable starting from node ID `0` (including node `0` itself).
3. Constructs an in-memory directed graph of this active subgraph.
4. Computes the PageRank of every node in this active subgraph.
   - Use a damping factor of $d = 0.85$.
   - Initialize all node PageRank values to $1.0 / N$, where $N$ is the number of nodes in the *active subgraph*.
   - Run exactly 25 iterations.
   - For nodes with no outgoing edges (sink nodes), their PageRank score is NOT redistributed (standard simplified PageRank).
5. Exports the results to `/home/user/pagerank_results.csv` with the header `node,pagerank` and each subsequent row containing the integer node ID and its PageRank score as a float/double (e.g., `5,0.00314`).

Compile your program to `/home/user/graph_analyzer` and execute it. 
Ensure the final CSV is perfectly formatted. Automated systems will parse it and evaluate the Mean Squared Error (MSE) of your PageRank scores against the true graph values.