You are a Database Reliability Engineer. Our primary graph database has suffered catastrophic corruption, but fortunately, we have the latest backup exported as raw CSV files. We need to verify the integrity of the backup by performing specific analytical queries on the graph topology. 

Since the graph database engine is currently offline, you must write a standalone C program that ingests the CSV data, reconstructs the graph relations, and calculates essential metrics using standard SQL analytical features (simulating Cypher/SPARQL graph traversals).

The backup consists of two files:
1. `/home/user/graph_nodes.csv` - Format: `id,label,name`
2. `/home/user/graph_edges.csv` - Format: `source_id,target_id,relationship_type`

Your task is to write a C program at `/home/user/verify_graph.c` that does the following:
1. Uses an embedded database library like SQLite (you will need to install any necessary C headers/libraries via `apt`, e.g., `libsqlite3-dev`).
2. Creates an in-memory database and loads the data from the two CSV files into appropriate tables.
3. Executes analytical queries to generate two reports.

**Report A: Dependency Paths (Simulating a Graph Traversal)**
Simulate a graph query equivalent to the Cypher: `MATCH (s:Server)-[:DEPENDS_ON]->(m:Service)-[:DEPENDS_ON]->(d:Database) RETURN s.name, d.name`
Using complex joins or CTEs, find all paths of length exactly 2 that start at a 'Server', pass through a 'Service', and end at a 'Database' via 'DEPENDS_ON' relationships.
Write the output to `/home/user/report_A.csv` in the format `server_name,database_name`. Order the results alphabetically by `server_name`, then by `database_name`.

**Report B: Node Degree Centrality Ranking (Window Functions & Pagination)**
Use SQL Window Functions to calculate the total degree (in-degree + out-degree) of every node in the graph. Rank the nodes based on their total degree in descending order using `DENSE_RANK()`.
Filter and paginate the results to return ONLY the top 5 highest-ranked nodes (Rank 1 to 5). If there are ties in rank, sort them secondarily by the node's `id` in ascending order.
Write the output to `/home/user/report_B.csv` in the format `rank,node_id,node_name,total_degree`.

Compile your C program to `/home/user/verify_graph` and execute it so that both CSV reports are generated accurately. Do not include headers in your output CSVs.