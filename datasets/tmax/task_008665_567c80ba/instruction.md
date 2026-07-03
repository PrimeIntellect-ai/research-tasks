You are a data engineer building an ETL pipeline to migrate hierarchical data from a legacy SQLite database into a Neo4j graph database.

You have been given a SQLite database file located at `/home/user/pipeline.db`.
The database contains a single table:
`CREATE TABLE assets (id INTEGER PRIMARY KEY, name TEXT, parent_id INTEGER);`
There is also an index: `CREATE INDEX idx_parent ON assets(parent_id);`

**The Problem:**
We recently bulk-inserted new rows, but a known SQLite bug caused the `idx_parent` index to become corrupted. Regular queries filtering or joining on `parent_id` are returning stale or missing rows. 

**Your Task:**
Create a Bash script at `/home/user/build_graph.sh` that accomplishes the following:
1. Rebuilds the corrupted indices in the SQLite database to ensure data consistency.
2. Executes a recursive hierarchical query (`WITH RECURSIVE`) to extract all assets that are descendants of the root asset (which has `id = 1`).
3. Filters the results to only include assets up to a maximum depth of 3 (where the root asset `id = 1` is depth 0).
4. Materializes this sub-graph into a Cypher script at `/home/user/insert.cypher`.

**Cypher Script Format:**
Your Bash script must generate the `/home/user/insert.cypher` file with the following strict formatting:
- First, print all node creation statements in the format: `MERGE (n:Asset {id: <id>, name: '<name>'});`
- Then, print all relationship statements in the format: `MERGE (c:Asset {id: <id>})-[:HAS_PARENT]->(p:Asset {id: <parent_id>});`
- The node statements must be sorted by `id` ascending.
- The relationship statements must be sorted by the child's `id` ascending.
- Do not create a relationship statement for the root asset (since its `parent_id` is NULL or it doesn't have a parent in the tree).

Make sure the bash script has executable permissions. When we run `/home/user/build_graph.sh`, it should seamlessly generate `/home/user/insert.cypher`.