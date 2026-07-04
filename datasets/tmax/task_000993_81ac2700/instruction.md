You are a database administrator tasked with optimizing and fixing a graph processing pipeline for an access control system. 

You have been provided with an SQLite database at `/home/user/access_graph.db` containing a knowledge graph of corporate network access.
The database has two tables:
- `nodes` (id TEXT PRIMARY KEY, label TEXT) -- Labels can be 'User', 'Role', 'Server', 'SecureDatabase'.
- `edges` (source TEXT, target TEXT, relation TEXT) -- Relations can be 'HAS_ROLE', 'CAN_ACCESS', 'CONNECTS_TO'.

Your predecessor wrote a query script that timed out and returned incorrect results because it performed an implicit cross join between all users and all databases, and failed to enforce the correct semantic path pattern.

Your task is to write a Python script at `/home/user/analyze_access.py` that correctly and efficiently computes the valid shortest access paths.

A path from a `User` to a `SecureDatabase` is only **valid** if it strictly follows this semantic pattern:
1. Exactly one `HAS_ROLE` edge from a `User` to a `Role`
2. Exactly one `CAN_ACCESS` edge from the `Role` to a `Server`
3. One or more `CONNECTS_TO` edges chaining from the `Server` to reach a `SecureDatabase`.

For example, a valid path looks like: `User -> [HAS_ROLE] -> Role -> [CAN_ACCESS] -> Server -> [CONNECTS_TO] -> Server -> [CONNECTS_TO] -> SecureDatabase`.
Paths that skip roles (e.g., User directly to Server) or use incorrect relations are invalid.

Your script must:
1. Extract the network topology from the database and perform graph traversal/pattern matching.
2. For every `User` in the database, calculate the shortest valid path length (minimum number of edges) to *any* `SecureDatabase`.
3. Count the total number of shortest valid paths from the `User` to any `SecureDatabase` (i.e., paths that have length equal to the user's minimum valid path length).
4. Aggregate the results and export them to `/home/user/access_summary.json`.

The output file `/home/user/access_summary.json` must be a JSON array of objects, sorted alphabetically by the `user` key. Filter out any users that have no valid paths to any SecureDatabase.
Format requirement:
```json
[
  {
    "user": "Alice",
    "min_hops": 4,
    "shortest_path_count": 2
  },
  ...
]
```

Use Python 3. You may use standard libraries and `networkx` (which you will need to install). Do not modify the original SQLite database.