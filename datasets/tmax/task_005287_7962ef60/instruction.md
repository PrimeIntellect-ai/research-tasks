You are a data engineer tasked with debugging and fixing an ETL pipeline step that processes a temporally-versioned Knowledge Graph. 

The raw data is stored in an SQLite database at `/home/user/kg_data.db`. The system uses a Type-2 Slowly Changing Dimension (SCD2) model to track the history of nodes and edges. 

Recently, the downstream graph analytics outputs have been corrupted with stale rows. A previously used materialized view has a corrupted index and incorrect timestamp logic, returning deactivated relationships.

Your task is to bypass the broken view and write a C++ program from scratch that extracts the correct, point-in-time snapshot of the graph, and performs a graph centrality analysis.

Here are the requirements:
1. **Dependencies:** You may need to install the SQLite3 development headers for C++ (`libsqlite3-dev` on Debian/Ubuntu).
2. **C++ Program:** Write a C++ program at `/home/user/process_kg.cpp`. 
3. **Point-in-Time Query:** Connect to `/home/user/kg_data.db` using the standard `sqlite3` C/C++ API. You must write a complex SQL query (using joins and subqueries if necessary) to retrieve only the "active" nodes and edges as of the UNIX timestamp `1700000000`.
   - A node or edge is considered active at time `T` if `valid_from <= T` and `valid_to > T`.
   - The tables are `nodes` (columns: `id`, `label`, `valid_from`, `valid_to`) and `edges` (columns: `source_id`, `target_id`, `type`, `valid_from`, `valid_to`).
   - Note: An edge is ONLY valid if both its source node and target node are ALSO active at time `T`. You must enforce this constraint in your SQL logic or application logic.
4. **Graph Analytics:** Using the active snapshot:
   - Calculate the `in_degree` and `out_degree` for every active node in the graph.
   - Calculate the `total_degree` (`in_degree` + `out_degree`).
   - Identify "Hub" nodes, defined as active nodes where the `total_degree` is `>= 3`.
5. **Output:** Write the identified Hub nodes to a CSV file at `/home/user/hubs.csv`.
   - The CSV must have exactly this header: `node_id,label,in_degree,out_degree,total_degree`
   - Sort the output rows primarily by `total_degree` in DESCENDING order, and secondarily by `node_id` in ASCENDING order.
   - Do not include spaces after the commas.

Compile your C++ program using `g++ process_kg.cpp -o process_kg -lsqlite3` and execute it so that the `/home/user/hubs.csv` file is generated.