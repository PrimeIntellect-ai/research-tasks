You are a database administrator tasked with replacing a legacy, unmaintained binary tool with an optimized Python implementation. 

We have an SQLite database located at `/home/user/topology.db` representing a hierarchical network topology. The database has two tables:
1. `nodes` (id INTEGER PRIMARY KEY, name TEXT, base_weight REAL)
2. `edges` (source_id INTEGER, target_id INTEGER, latency REAL) - representing directed connections.

Currently, we rely on a compiled, stripped executable located at `/app/legacy_flow_calc` to compute a proprietary "Flow Centrality" metric for a given starting node. The binary takes a node ID as a command-line argument, queries the database, and prints a single floating-point number representing the result. It is incredibly slow because it performs N+1 queries.

Your task:
1. Analyze the behavior of `/app/legacy_flow_calc` to deduce how it calculates the Flow Centrality metric for a given root node. It relies on traversing the network hierarchy (you will likely need recursive CTEs to do this efficiently in SQL).
2. Write an optimized Python script at `/home/user/optimized_flow.py` that takes a single integer argument (the starting node ID).
3. Your script must connect to `/home/user/topology.db`, perform the equivalent calculation using parameterized queries and optimized SQL (leveraging recursive CTEs and joins rather than Python-side loops), and print only the final computed floating-point value to stdout (rounded to 4 decimal places).
4. Ensure your script output is bit-exact equivalent to the legacy binary for any valid node ID, but executes significantly faster by pushing the graph traversal logic into the database engine.