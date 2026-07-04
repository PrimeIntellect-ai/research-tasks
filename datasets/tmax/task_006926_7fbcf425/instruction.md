You are a data engineer working on an ETL pipeline for a graph processing system. 

We have an SQLite database located at `/home/user/graph.db` containing a single table:
`edges (src INTEGER, dst INTEGER, weight INTEGER)`

There is an index on the `src` column named `idx_src`. Due to a storage failure, this index has become corrupted. Any SQLite `SELECT` query that relies on `idx_src` (such as `GROUP BY src` or filtering by `src` without forcing table scans) returns stale and incorrect duplicate rows. 

Your task is to:
1. Extract the true edge list from the `edges` table in `/home/user/graph.db` by explicitly bypassing the corrupted index (e.g., using the `NOT INDEXED` clause).
2. Write a C program located at `/home/user/process_graph.c` that reads this materialized edge list from standard input (expected format: `src|dst|weight` or `src dst weight`).
3. The C program must aggregate the outgoing edges to compute the total weighted out-degree for each `src` node. Node IDs are guaranteed to be integers between 1 and 100,000.
4. The C program should output the single node ID with the highest total weighted out-degree, along with that weight.
5. Compile your C program and run your extraction pipeline, saving the final summarized output to `/home/user/max_degree.txt`.

The output file `/home/user/max_degree.txt` must contain exactly one line in the following format:
`Node: <node_id>, Total Weight: <max_weight>`

Do not use any external C libraries beyond the standard library (`stdio.h`, `stdlib.h`, etc.).