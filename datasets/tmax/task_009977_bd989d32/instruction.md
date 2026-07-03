You are a data engineer responsible for a new C-based ETL pipeline. We have an SQLite database located at `/home/user/network_staging.db` which contains a raw property graph from a legacy system. 

Recently, we discovered that one of the critical indexes in this database has become logically corrupted during an interrupted migration. The query optimizer still attempts to use this index, which can result in stale or partial row returns if a query plan relies on it.

Your objective is to reverse-engineer the schema, bypass the corrupted index, and perform a graph analytics extraction using C.

**Phase 1: Data Model Reverse Engineering & Query Optimization**
1. Inspect the database `/home/user/network_staging.db` using the `sqlite3` CLI. 
2. Identify the primary table storing the graph edges. The table name starts with `etl_edges_`.
3. Identify the corrupted index on the source node column.
4. Formulate a query that retrieves all valid edges (where the `status` column equals 'ACTIVE') while explicitly preventing the SQLite query optimizer from using the corrupted index. You must force a full table scan or explicitly drop the index before querying.

**Phase 2: Graph Analytics via C API**
1. Write a C program at `/home/user/extract_centrality.c`.
2. The program must use the `sqlite3` C API (`<sqlite3.h>`) to connect to `/home/user/network_staging.db`.
3. Execute your optimized query to retrieve all active edges. 
4. In memory, compute the **out-degree centrality** (the number of outgoing active edges) for every source node present in the active edges.
5. Write the results to a CSV file at `/home/user/out_degree.csv`.

**Output Requirements:**
- The compiled binary must be located at `/home/user/extract_centrality`.
- You can compile using `gcc /home/user/extract_centrality.c -o /home/user/extract_centrality -lsqlite3`.
- The output file `/home/user/out_degree.csv` must have the header `node_id,out_degree`.
- The rows must be sorted in **descending order** of `out_degree`. If there is a tie, sort by `node_id` in **ascending order**.
- Only nodes with at least 1 outgoing active edge should be included.

*Note: You do not have root access. Standard build tools (`gcc`, `make`) and `libsqlite3-dev` are already installed on the system. You may use shell commands to explore the database before writing your C program.*