You are acting as a compliance officer auditing an internal permissions database. You have been provided with a SQLite database at `/home/user/compliance.db`. 

There is an existing SQL query in `/home/user/bad_query.sql` that is meant to list all direct asset accesses for users in the 'Compliance' department. However, it is returning millions of rows because of a missing join condition (an implicit cross join).

Your task has three parts:

1. **Reverse Engineer & Fix the Query:** 
   Analyze the schema of `/home/user/compliance.db`. Identify the missing join condition in `/home/user/bad_query.sql` and write the corrected SQL query to `/home/user/fixed_query.sql`. The corrected query must return exactly two columns: `user_name` and `asset_name`, representing only the valid direct accesses for users in the 'Compliance' department.

2. **Graph Traversal via C++:**
   The compliance team suspects a privilege escalation path exists due to nested group trusts. 
   Write a C++ program at `/home/user/path_finder.cpp` that reads `/home/user/compliance.db` (using the `sqlite3` C API) and builds a directed graph of permissions.
   The graph should map the following directed edges:
   - User -> Group (via user_groups)
   - Group -> Group (via group_trusts, where a group inherits permissions from a trusted group)
   - Group -> Asset (via group_assets)
   
   Using this graph, compute the shortest path (fewest edges) from the user named `"Mallory"` to the asset named `"Mainframe"`. 

3. **Export the Results:**
   Compile your program to `/home/user/path_finder` and run it.
   Your C++ program must output the shortest path as a comma-separated string of node names to the file `/home/user/shortest_path.txt`. 
   For example, if the path goes from Mallory to GroupA to GroupB to Mainframe, the file should contain exactly: `Mallory,GroupA,GroupB,Mainframe`

Notes:
- You may use `g++` and standard libraries. Link the SQLite library using `-lsqlite3`.
- Ensure your C++ program cleanly handles the database connection and avoids memory leaks.