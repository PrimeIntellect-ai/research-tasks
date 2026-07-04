You are an expert data analyst and C developer. You have been given a task to compute the shortest network latency between two critical servers in a complex, hierarchical network topology.

You are provided with a massive edge list in a CSV file at `/app/data/network.csv`. The file has no header and contains three columns: `source_node` (string), `target_node` (string), and `latency` (float).

Because the dataset is large and we want a standalone, high-performance binary, you must use C and embed SQLite to perform the analysis. 

Your tasks are:
1. We have vendored the SQLite amalgamation source code in `/app/sqlite/`. It contains a build script `/app/sqlite/build.sh` that is supposed to compile a given C file with the SQLite amalgamation. However, this script is currently broken and fails to link properly. Find and fix the error in `/app/sqlite/build.sh`.
2. Write a C program at `/home/user/shortest_path.c` that:
   - Embeds SQLite using the header from `/app/sqlite/sqlite3.h`.
   - Creates an in-memory SQLite database.
   - Parses the `/app/data/network.csv` file and loads the data into a table named `edges` with columns `source`, `target`, and `latency`.
   - Executes an advanced SQL query (using a Recursive Common Table Expression) to compute the shortest path (minimum total latency) from the node named `NODE_START` to the node named `NODE_END`. Note that the graph is directed.
   - Writes *only* the final minimum total latency as a floating-point number (e.g., `45.23`) to `/home/user/min_latency.txt`.

Constraints & Guidelines:
- You must use standard C (C99 or C11).
- Use bash to execute your compilation and run your binary.
- Ensure your recursive CTE handles potential cycles or limits depth if necessary, though the shortest path should be bounded by the minimum latency logic. 
- The target verifier will strictly check the numerical value in `/home/user/min_latency.txt`.