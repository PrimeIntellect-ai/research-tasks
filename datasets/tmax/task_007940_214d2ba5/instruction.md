You are a Database Reliability Engineer investigating an issue with our microservice dependency tracker. We have an SQLite backup database located at `/home/user/service_mesh.db`. 

Recently, a bug caused stale dependency records to be queried. The database contains historical versions of edge connections between services. You need to reconstruct the true, current dependency graph and identify the most critical services.

Your task:
1. **Reverse Engineer the Schema**: Inspect `/home/user/service_mesh.db` to understand the table structures. There are tables for services and their dependencies.
2. **Filter Stale Rows (Data Querying)**: The dependencies table contains multiple versions for the same `(source_id, target_id)` pairs. Write a query using window functions to extract only the latest version (highest `version` number) for each pair. 
3. **Graph Projection**: Filter this latest set of edges to include only those where `is_active = 1`. Treat these as a directed graph where edges point from `source_id` to `target_id`.
4. **Graph Analytics**: Using Python, calculate the **in-degree** (number of incoming edges) for every service in this active graph.
5. **Output**: Find the top 3 services with the highest in-degree. Write their service names to `/home/user/critical_services.txt`, one name per line, sorted in descending order of their in-degree. In case of a tie, sort alphabetically by service name.

Constraints:
- Use Python for the graph processing and querying.
- Do not install external graph libraries like `networkx` if you can avoid it; standard dictionary-based adjacency lists are sufficient for in-degree, but you may use `sqlite3`.