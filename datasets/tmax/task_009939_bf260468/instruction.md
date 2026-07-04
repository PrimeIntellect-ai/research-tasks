You are an AI assistant helping a data researcher clean and organize a graph dataset. 

The researcher has an SQLite database located at `/home/user/graph_data.db`. This database contains an `edges` table with the following schema:
- `id` (INTEGER PRIMARY KEY)
- `source` (INTEGER)
- `target` (INTEGER)
- `weight` (REAL)
- `recorded_at` (INTEGER) - A UNIX timestamp representing when the edge was recorded.

Because of a data collection issue, there are multiple records for the same `(source, target)` pair over time. The researcher only wants the **most recent** edge (highest `recorded_at`) for each `(source, target)` pair. Furthermore, they only want edges where this most recent weight is greater than or equal to a specific threshold.

Your task is to:
1. Write a C++ program at `/home/user/process_graph.cpp` that queries this SQLite database.
2. The program must take a single command-line argument: a `double` representing the minimum weight threshold.
3. Use a single SQL query equipped with **window functions** (e.g., `ROW_NUMBER()`) to analytically deduce the latest weight for each `(source, target)` pair, and filter the final results using a **parameterized query** where the command-line threshold is bound to the statement safely.
4. The C++ program should print the matching edges to standard output in the format `source,target,weight` (one per line, with no spaces).
5. Compile your C++ program using `g++` (link with `-lsqlite3`) to an executable named `/home/user/process_graph`.
6. Finally, execute your program with a threshold of `10.5` and pipe its output into the `sort` command to sort the output numerically by `source` (first column) and then by `target` (second column). Redirect the final sorted pipeline output to `/home/user/final_edges.csv`.

Ensure your C++ code gracefully handles SQLite connections and strictly uses parameterized binding for the threshold to prevent SQL injection or type conversion issues.