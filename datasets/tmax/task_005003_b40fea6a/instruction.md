You are a data analyst tasked with processing a set of large CSV files representing a dependency graph (nodes and directed edges). To do this efficiently, our team relies on a custom C utility that loads these CSVs into an in-memory SQLite database and computes the transitive closure (all reachable dependencies) for a given starting node using a recursive Common Table Expression (CTE).

We recently migrated our build server, and the utility is now failing to compile and run correctly. The source code for the tool is vendored at `/app/csv-graph-toolkit`. 

Your objectives are:
1. Fix the build configuration. The `Makefile` in `/app/csv-graph-toolkit` is currently broken. It fails to link the included `sqlite3.c` amalgamation file and complains about missing libraries. You must modify the Makefile so that running `make` successfully produces the executable `graph_query`.
2. Fix the querying logic. The file `graph_query.c` has a bug in its SQL query. It is supposed to use a recursive CTE to find all nodes reachable from a given parameter `?1`. However, the query was badly modified by a previous developer (it currently has an infinite loop or incorrect join condition referencing a corrupted index logic). Rewrite the SQL string inside `graph_query.c` so that it correctly traverses the `edges` table recursively. The table `edges` has columns `source_id` (TEXT) and `target_id` (TEXT). The query should return a single column containing the `target_id` of all reachable nodes, sorted alphabetically.
3. Once fixed and compiled, move the resulting executable to `/home/user/graph_query`.

The program is designed to take a single command-line argument (the starting `source_id`) and print the reachable nodes one per line to standard output. 

Ensure that your compiled `/home/user/graph_query` perfectly matches the expected behavior for any valid node ID, as an automated system will aggressively test it with random node IDs.