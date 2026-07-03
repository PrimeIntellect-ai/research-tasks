You are a data analyst investigating a routing network. The network data is stored in an SQLite database at `/home/user/data/network.db`. The database contains two tables: `nodes(id, name)` and `edges(source, target, weight)`. 

Recently, the database suffered an index corruption. The index `idx_edges_src` on the `edges` table is corrupted and returns stale, incorrect weights when queried using index scans. You must extract the true, underlying table data (bypassing or dropping the corrupted index).

Furthermore, we received a patch of recent network changes in `/home/user/data/updates.csv` (format: `source,target,new_weight`). These updates supersede any existing edges in the database, and may introduce new edges.

We need to compute the shortest path distances for 100 node pairs listed in `/home/user/data/queries.csv` (format: `source,target`).

To compute the paths, a proprietary, stripped routing engine is provided at `/app/path_oracle`. This binary acts as an interactive oracle: it reads graph construction and query commands from `stdin` and writes results to `stdout`. However, the documentation for its exact input protocol has been lost. You will need to reverse-engineer its expected text-based input format by inspecting the binary (e.g., using `strings`, `strace`, or `objdump`).

Your task:
1. Recover the true edge data from `network.db`, ignoring the corrupted index.
2. Apply the updates from `updates.csv`.
3. Reverse-engineer the input protocol for `/app/path_oracle`.
4. Feed the reconstructed graph and the queries to the oracle.
5. Save the output distances for the 100 queries in `/home/user/results.csv` in the exact format: `source,target,distance`. If no path exists, the distance should be `-1`.

Ensure your final output is perfectly formatted, as it will be evaluated programmatically for accuracy against a golden dataset.