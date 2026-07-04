You are acting as a Database Administrator for a microservices architecture team. We track service dependencies using a custom SQLite-based knowledge graph. Recently, we've been experiencing distributed transaction deadlocks because some services have circular dependencies. 

Your task is to identify specific "triangle" deadlocks (where Service A depends on Service B, Service B depends on Service C, and Service C depends on Service A) using our database.

The database is located at `/home/user/graph.db` and has the following schema:
- `Nodes` (id INTEGER PRIMARY KEY, name TEXT)
- `Edges` (source_id INTEGER, target_id INTEGER, relation_type TEXT)

Write a Python script at `/home/user/analyze_graph.py` that meets these requirements:
1. It must accept a single command-line argument: the `relation_type` to search for (e.g., `DEPENDS_ON`).
2. It must execute a **single parameterized SQL query** using complex joins to find all triangle cycles (A -> B -> C -> A) matching the provided relation type. Do not use string concatenation for the relation type; you must use parameterized queries to prevent SQL injection and query plan cache misses.
3. To prevent duplicate reporting of the same cycle (e.g., A-B-C, B-C-A, C-A-B), your SQL query must enforce that the `id` of node A is strictly less than the `id` of node B, and the `id` of node A is strictly less than the `id` of node C.
4. Process the results and output them to `/home/user/cycles.json`. The output must be a JSON array of lists, where each inner list contains the `name` of the three nodes in the cycle, in the order A, B, C.
5. Sort the final JSON array alphabetically by the first node's name, then the second node's name, then the third.

Execute your script by running: `python /home/user/analyze_graph.py DEPENDS_ON`

Leave the resulting `/home/user/cycles.json` file in place for verification.