You are a data engineer building an ETL pipeline to process dependency graph data. 

We have a SQLite database located at `/home/user/graph.db` containing two tables representing a knowledge graph of software dependencies:
- `packages` (id INTEGER PRIMARY KEY, name TEXT)
- `dependencies` (pkg_id INTEGER, depends_on_id INTEGER)

There is a partially written C program at `/home/user/extract_deps.c` that is supposed to extract all transitive dependencies (dependencies of dependencies, recursively) for a given package name using a parameterized query. 

However, the current implementation is incomplete and inefficient:
1. The SQL query in the C code lacks the proper recursive CTE (Common Table Expression) to traverse the knowledge graph.
2. The parameterized query binding is missing, so it doesn't correctly substitute the target package name provided as a command-line argument.
3. The database is missing necessary indexes, making graph traversal extremely slow.

Your task is to:
1. Analyze the query plan for a recursive traversal and create the optimal index(es) directly in the `/home/user/graph.db` database to speed up `dependencies` lookups.
2. Fix the C program `/home/user/extract_deps.c`:
   - Write a Recursive CTE in the SQL string that finds all transitive dependencies for the parameterized package name. The CTE must return two columns: `depth` (integer, starting at 1 for direct dependencies) and `name` (string, the name of the dependency).
   - Correctly bind the package name to the parameterized query using `sqlite3_bind_text`.
   - Iterate through the results and write them to a file named `/home/user/etl_output.csv` in the format `depth,name` (one per line, ordered by depth ASC, then name ASC).
3. Compile the C program using `gcc -o /home/user/extract_deps /home/user/extract_deps.c -lsqlite3`.
4. Run the compiled program for the package named `lib_alpha`: `/home/user/extract_deps lib_alpha`.

Ensure the final output file `/home/user/etl_output.csv` exactly matches the required format and contains the correct hierarchical data.