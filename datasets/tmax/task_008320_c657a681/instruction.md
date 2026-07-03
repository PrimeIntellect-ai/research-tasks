You are a data engineer tasked with optimizing the execution schedule of an ETL pipeline. The metadata for the pipeline jobs is stored in a SQLite database located at `/home/user/etl_metadata.db`. 

The database contains a single table:
`jobs(id INTEGER PRIMARY KEY, target_table TEXT, sql_query TEXT)`

Each row represents an ETL job that populates the `target_table` using the `sql_query`. 

Your objective is to reverse engineer the data model dependencies from the SQL queries, build a dependency graph, and find the shortest execution path between two specific tables.

Follow these steps:
1. **Data Model Reverse Engineering**: A table depends on any source table that provides data to it. You can identify source tables by looking at the `sql_query` column. Extract any table name that immediately follows a `FROM` or `JOIN` keyword (assume keywords are uppercase, separated by a single space from the table name, and table names consist only of alphanumeric characters and underscores `[a-zA-Z0-9_]+`).
2. **Graph Traversal**: Write a C++ program at `/home/user/optimizer.cpp` that reads from the SQLite database, parses the dependencies, and builds a directed graph. An edge should point from the source table to the `target_table`.
3. Compute the shortest path (fewest number of edges) from `raw_clicks` to `executive_dashboard`.
4. **Output Schema Validation & Pipeline Chaining**: Have your C++ program output the result directly to a JSON file at `/home/user/pipeline.json`. The JSON must strictly validate against this exact format (no whitespace or newlines inside the structure, just a single minified line):
`{"pipeline":["raw_clicks","intermediate_table_1","intermediate_table_2","executive_dashboard"]}`

You may install `libsqlite3-dev` or any other standard packages using `sudo apt-get` if required to compile your C++ code. Compile your program, execute it, and ensure `/home/user/pipeline.json` is created correctly.