You are a data analyst tasked with processing graph-like relational data for an internal knowledge base. 

You have been given a SQLite database `/home/user/graph_data/knowledge.db` which contains two tables:
1. `nodes` (id TEXT PRIMARY KEY, type TEXT, properties_json TEXT)
2. `edges` (source TEXT, target TEXT, weight REAL, updated_at INTEGER)

**The Problem:**
Due to a previous bug, the database currently suffers from a "stale rows" issue. The `edges` table lacks a proper uniqueness constraint, and multiple rows exist for the same `(source, target)` pair. Only the row with the highest `updated_at` timestamp for a given `(source, target)` pair is valid; the rest are stale.

Additionally, you have a CSV file at `/home/user/graph_data/new_edges.csv` containing new edge data that must be integrated.

**Your objectives:**

1. **Clean Stale Rows & Apply Index Strategy:** 
   Write a Python script `/home/user/process_graph.py` that connects to the SQLite database and deletes all stale rows in the `edges` table. 
   After cleaning, the script must create a `UNIQUE INDEX` named `idx_unique_edges` on the `(source, target)` columns to enforce uniqueness and optimize future upserts.

2. **Parameterized Updates:**
   Your Python script must read `/home/user/graph_data/new_edges.csv` (which has columns `source,target,weight,updated_at`) and insert this data into the `edges` table. You must use **parameterized queries** to prevent injection and handle potential conflicts. If an edge already exists, update its `weight` and `updated_at` ONLY if the CSV's `updated_at` is strictly greater than the existing record's `updated_at`.

3. **Knowledge Graph Pattern Matching:**
   Using a recursive CTE in SQLite, query the newly cleaned and updated database to find all nodes that are downstream (reachable via directed edges) from the source node ID `ROOT_42`. 
   For each reachable node, calculate the minimum number of "hops" (edges) from `ROOT_42`. `ROOT_42` itself should not be in the output unless it loops back to itself.

4. **Output:**
   Save the results of your graph traversal as a JSON file at `/home/user/graph_data/downstream_nodes.json`. The JSON should be a dictionary where the keys are the reachable node IDs (strings) and the values are their minimum hop counts (integers).

**Environment Details:**
- Python 3 is available. You may use the built-in `sqlite3` and `csv` modules.
- Ensure all file paths referenced in your code use absolute paths.