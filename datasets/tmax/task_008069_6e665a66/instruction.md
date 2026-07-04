You are a database administrator tasked with optimizing and fixing a broken reporting process. 

A previous engineer wrote a script (`/home/user/bad_report.py`) to calculate the total network traffic along a specific routing path. However, they didn't understand the database schema and used an implicit cross join without proper conditions, which caused the query to return astronomically large, incorrect results and consume massive resources.

Your objectives are:
1. **Reverse Engineer the Database:** Analyze the SQLite database located at `/home/user/network.db` to understand its schema. It contains information about servers, network connections (which form a directed graph), and traffic logs.
2. **Graph Traversal:** Write a Python script to compute the shortest routing path (minimum number of hops) from the server with the hostname `'Gateway-01'` to the server with the hostname `'Database-Cluster'`. 
3. **Cross-query Aggregation:** Once you have the shortest path, construct a new, optimized Python script using parameterized SQL queries to calculate the total sum of `bytes_transferred` from the traffic logs, but **only** for the specific sequence of network connections (edges) that make up your computed shortest path.
4. **Output:** Create a JSON file at `/home/user/solution.json` containing the exact shortest path and the corrected aggregated traffic total.

The format of `/home/user/solution.json` must be strictly as follows:
```json
{
  "shortest_path": ["Gateway-01", "some-intermediate-node", "...", "Database-Cluster"],
  "total_traffic": 12345
}
```

Do not modify `/home/user/bad_report.py`. Write your own scripts to solve the problem and generate the final JSON file. Ensure all data retrieval dynamically uses parameterized SQL queries.