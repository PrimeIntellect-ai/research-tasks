You are a database administrator and data engineer. You have been brought in to fix a broken network routing report and optimize the underlying routing data pipeline.

In `/home/user/network.db` (an SQLite database), there are two tables:
1. `servers` (`id` INTEGER PRIMARY KEY, `name` TEXT)
2. `links` (`source_id` INTEGER, `target_id` INTEGER, `bandwidth` REAL)

A junior developer wrote a SQL query to extract the network topology for routing analysis. However, the query is producing millions of rows because it contains a classic SQL anti-pattern: an implicit cross join. 

The broken query is located at `/home/user/buggy_query.sql`.

Your task consists of three parts:

**Part 1: Fix the SQL Query**
Create a new file `/home/user/fixed_query.sql`. Write a corrected SQLite query that:
1. Properly joins the tables to return `source` (the name of the source server), `target` (the name of the target server), and `bandwidth`.
2. Uses a window function to filter the results so that it ONLY returns the top 2 links with the highest `bandwidth` per source server. If there is a tie in bandwidth, resolve it by ordering the `target` name in ascending alphabetical order.

**Part 2: Export Data**
Execute your fixed query against `/home/user/network.db` and export the results to `/home/user/graph.json`. The output must be a JSON array of objects, where each object looks exactly like: `{"source": "...", "target": "...", "bandwidth": ...}`. You can write a small script to do this or use sqlite3 CLI features.

**Part 3: Compute Shortest Path**
Write a Python script at `/home/user/solve_path.py` that reads `/home/user/graph.json` and performs a graph traversal to find the shortest path from the server named `'Start'` to the server named `'End'`.
* The graph is directed.
* The "cost" of traversing an edge is calculated dynamically using parameterized logic: `cost = 10000.0 / bandwidth`.
* Use Dijkstra's algorithm (or a similar valid shortest path algorithm) to find the path with the lowest total cost.

The script must write the final calculated path and total cost to `/home/user/result.json` in the following exact JSON format:
```json
{
  "path": ["Start", "IntermediateNode", "End"],
  "cost": 123.45
}
```

Ensure all files (`fixed_query.sql`, `graph.json`, `solve_path.py`, and `result.json`) are left in `/home/user/` when you are finished.