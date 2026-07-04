I am building an ETL pipeline that processes graph data, and I need your help to fix a vendored C library and write a high-performance C program to analyze the graph structure. 

We have a custom graph query library vendored at `/app/libgraphquery-1.2.0/`. It provides a wrapper around SQLite for running complex analytics on graph datasets. However, the package is currently broken. First, the `Makefile` has a syntax error that prevents it from compiling. Second, the query optimization logic in `src/query_planner.c` has a missing patch that prevents index utilization for analytical window functions. 

Your task is to:
1. Fix the `Makefile` in `/app/libgraphquery-1.2.0/`.
2. Fix the missing patch in `src/query_planner.c` so that it properly pushes down index bounds for window functions.
3. Write a C program at `/home/user/etl_graph_processor.c` that links against this library. 
4. The C program must compile to `/home/user/etl_graph_processor`.

The `etl_graph_processor` executable must accept two arguments:
`./etl_graph_processor <input_csv_file> <output_csv_file>`

The executable should do the following:
- Ingest a graph edge list (Source, Target, Weight) from the `<input_csv_file>`.
- Use the library's functions to create an optimized index strategy (you must explicitly create indexes on the Source and Target columns).
- Execute a query using window functions to compute the "Ranked Centrality" of each node. The Ranked Centrality is defined as the sum of incoming edge weights, partitioned by the Target node, ranked descending.
- Write the results to the `<output_csv_file>` in the format `NodeID,RankedCentrality`.

Please ensure your program strictly conforms to the expected output format, as it will be heavily tested against random graph datasets to verify bit-exact correctness.