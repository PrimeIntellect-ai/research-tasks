You are a database administrator working with an SQLite database containing social network data. The database is located at `/home/user/social_network.db`. 

The database has two tables:
1. `users(user_id INTEGER PRIMARY KEY, profile_json TEXT)`
2. `connections(user_id INTEGER, friend_id INTEGER, interaction_score INTEGER)`

There are some performance issues and data extraction requests from the analytics team. Please complete the following tasks:

1. **Index Optimization**: The `connections` table currently has some inefficient indexes. Identify and drop all existing indexes on the `connections` table. Then, create a single, highly efficient covering index named `idx_cover` on the `connections` table to optimize queries that filter by `user_id` and retrieve both `friend_id` and `interaction_score`.

2. **Graph Traversal Querying**: Write a Python script at `/home/user/pipeline.py` that connects to this database and performs the following operations:
   - Uses a recursive CTE (Common Table Expression) to find the shortest path (fewest hops) from `user_id = 10` to `user_id = 42`.
   - If there are multiple paths with the same minimum number of hops, choose the one with the highest total `interaction_score` along the path.
   - Write the optimal path as a comma-separated sequence of `user_id`s (e.g., `10,5,42`) to a file at `/home/user/path.txt`.
   - For each user in this optimal path, extract their `profile_json` from the `users` table. Parse the JSON document, inject a new key `"path_order"` representing their 0-indexed position in the path (e.g., 0 for the start node, 1 for the next, etc.), and output the resulting list of JSON objects to `/home/user/path_profiles.json` in a valid JSON array format.

Ensure your Python script runs successfully and produces the required output files. You may use the standard `sqlite3` and `json` libraries in Python.