You are a database administrator tasked with optimizing a graph analytics workload. 

We have an SQLite database located at `/home/user/graph.db`. It contains a single table `edges(src INTEGER, dst INTEGER)` representing a directed knowledge graph. 

There is a C program located at `/home/user/triangle_analyzer.c` that connects to this database and executes a pattern matching query to find the node that participates in the highest number of directed triangles (a cycle of length 3: A->B, B->C, C->A). 

Currently, the query runs extremely slowly because the database lacks proper indexing, and the database optimizer is resorting to full table scans. Furthermore, an old index (`idx_stale`) was created incorrectly and is causing suboptimal query plans.

Your objectives:
1. Examine the database and remove any unhelpful or corrupted indexes.
2. Create the optimal index(es) on the `edges` table to speed up the triangle pattern matching query. 
3. Modify the `/home/user/triangle_analyzer.c` program so that it does the following:
   a. First, executes `EXPLAIN QUERY PLAN` on the triangle counting query and writes the literal `detail` column of the query plan output to a file named `/home/user/query_plan.txt` (one line per step).
   b. Then, executes the actual triangle counting query and writes the result to `/home/user/max_triangle.txt` in the exact format: `NodeID,TriangleCount` (e.g., `42,15`).
4. Compile your program using `gcc -O2 -o /home/user/triangle_analyzer /home/user/triangle_analyzer.c -lsqlite3`.
5. Run the compiled executable so that the output files are generated.

The triangle counting query should conceptually match:
`SELECT e1.src, COUNT(*) as triangles FROM edges e1 JOIN edges e2 ON e1.dst = e2.src JOIN edges e3 ON e2.dst = e3.src WHERE e3.dst = e1.src GROUP BY e1.src ORDER BY triangles DESC LIMIT 1;`

Ensure both output files exist and contain the correct optimized query plan and the correct analytics result.