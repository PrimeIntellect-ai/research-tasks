You are a data analyst managing a graph database stored in an SQLite file at `/home/user/graph.db`. 

The database contains a single table tracking historical edge records:
`CREATE TABLE edges (src TEXT, dst TEXT, relation TEXT, timestamp INTEGER, is_deleted INTEGER);`

Currently, the database has a poorly designed index:
`CREATE INDEX bad_idx ON edges(src);`

This index causes severe performance issues and doesn't adequately support filtering out stale data. Whenever an edge is updated or removed, a new row is inserted with a newer `timestamp`. An edge is considered currently active if its *most recent* row has `is_deleted = 0`. If the most recent row has `is_deleted = 1`, the edge does not exist.

Your task is to write a C program `/home/user/query_graph.c` that functions as a query pipeline to do the following:
1. Connect to `/home/user/graph.db`.
2. Drop the existing `bad_idx`.
3. Create a highly optimized covering index named `good_idx` that dramatically speeds up finding the latest active edges for a given relation.
4. Execute an SQL query (acting as a graph query similar to Cypher's `MATCH (a)-[:KNOWS]->(b)-[:KNOWS]->(c)-[:KNOWS]->(a) RETURN a,b,c`) to find all active triangles of the `KNOWS` relation. 
5. Output the resulting triangles to a CSV file at `/home/user/triangles.csv` with the header `node1,node2,node3`.

Requirements for the C program:
- Only consider the *latest* row for each `(src, dst)` pair. Ignore all older rows for that pair.
- The edges forming the triangle must have `relation = 'KNOWS'`.
- Sort the columns in the output such that `node1 < node2 < node3` for each row (you can handle this lexicographical ordering in the SQL query itself using `MIN`, `MAX`, etc., or in C).
- Sort the rows in the final CSV file lexicographically by `node1`, then `node2`, then `node3`.
- The CSV file should be comma-separated without spaces.
- Compile your program using `gcc /home/user/query_graph.c -lsqlite3 -o /home/user/query_graph` and run it. 

Ensure the final output file `/home/user/triangles.csv` exactly matches the required format.