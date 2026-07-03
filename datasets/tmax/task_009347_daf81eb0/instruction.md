You are a Data Engineer building out an ETL pipeline. Recently, our downstream systems have been receiving stale and incorrect data from a materialized graph view stored in an SQLite database.

There is an SQLite database located at `/home/user/etl_data.db`. It contains three tables representing a hierarchical data graph:
1. `nodes` (`id` INTEGER PRIMARY KEY, `weight` INTEGER)
2. `edges` (`source` INTEGER, `target` INTEGER) - Represents the true directed edges between nodes.
3. `materialized_paths` (`source` INTEGER, `target` INTEGER, `total_weight` INTEGER, `is_valid` INTEGER) - A flattened, projected table storing the pre-computed sum of node weights along the *shortest path* (by node weight sum, inclusive of the source and target nodes) between any two nodes. 

Due to a bug in a previous migration, the `materialized_paths` table contains corrupted `total_weight` values and "ghost" paths (pairs of nodes that are no longer reachable). 

Your task is to write a C++ program at `/home/user/graph_etl.cpp` that performs the following:
1. Connects to `/home/user/etl_data.db`.
2. Loads the true graph from `nodes` and `edges`.
3. Performs a graph traversal to compute the true shortest path weight (summing the `weight` of all nodes on the path, including source and target) for every pair of nodes present in the `materialized_paths` table.
4. Updates the `materialized_paths` table:
   - If a path exists, correct the `total_weight` to the accurate shortest path weight and ensure `is_valid` is set to `1`.
   - If a path does *not* exist between the source and target in the true graph, set `is_valid` to `0` and leave `total_weight` as is.
5. Computes a cross-query aggregation: calculate the sum of the `total_weight` column for all rows in `materialized_paths` where `is_valid = 1` *after* your updates.
6. Writes this final integer sum to `/home/user/aggregation_result.txt`.

You must install any necessary C++ SQLite libraries (e.g., using `apt-get`). Compile your code to `/home/user/graph_etl` and run it to complete the ETL job.

Constraints:
- You may use standard C++ libraries and libsqlite3.
- The path weight is defined as the sum of node weights. If there are multiple paths, use the minimum sum.
- Output only the raw integer in `/home/user/aggregation_result.txt`.