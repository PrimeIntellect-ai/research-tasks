You are acting as a Database Administrator and Data Engineer. We have a locally stored knowledge graph in an SQLite database at `/home/user/graph.db`. This database models a microservice architecture and its dependencies. 

Currently, our data retrieval pipeline is extremely slow. It uses multiple queries in a loop to traverse the graph and find all transitive dependencies (up to depth 3) for every node of type 'Service'. 

Your task is to optimize this process by combining query optimization, knowledge graph pattern matching via SQL, and Python pipeline construction.

Here are your objectives:
1. **Analyze and Optimize the Database:** The database has two tables: `Nodes(id TEXT PRIMARY KEY, type TEXT)` and `Edges(source_id TEXT, target_id TEXT, relation_type TEXT)`. Add appropriate index(es) to the `Edges` table to optimize traversal by `source_id` and `relation_type`.
2. **Write an Optimized Python Pipeline:** Create a Python script at `/home/user/fast_pipeline.py` that connects to `/home/user/graph.db`. 
    - Instead of doing N+1 queries, you must write a **single SQL query** using a Recursive Common Table Expression (CTE) to find all dependencies (relation_type = 'depends_on') up to a maximum depth of 3, starting from all nodes where `type = 'Service'`.
    - The Python script must execute this query and process the results into a dictionary mapping each Service's `id` to a deduplicated, ascending-sorted list of its dependency `id`s (excluding the starting service itself).
    - The script must save this dictionary as a JSON file at `/home/user/optimized_results.json`.
3. **Capture the Query Plan:** Run `EXPLAIN QUERY PLAN` on your optimized recursive CTE query. Save the exact text output of this query plan to `/home/user/query_plan.txt`.

Ensure your Python script is executable and runs successfully. The automated tests will verify the existence of the database indexes, the contents of `optimized_results.json`, and the query plan log.