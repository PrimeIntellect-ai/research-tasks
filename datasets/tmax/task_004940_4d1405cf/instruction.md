You are acting as a data engineer. We have a C-based query engine that processes graph data stored in CSV files using an embedded SQLite database. However, the current implementation has a bug: it produces incorrect aggregation results due to an implicit cross join in the SQL query, and it runs extremely slowly on larger datasets.

Your task is to fix and optimize the C program located at `/home/user/graph_analyzer.c`. 

Here are the details:
1. The program accepts one command-line argument: the path to a directory containing `nodes.csv` and `edges.csv`.
2. `nodes.csv` has the format: `node_id,category,value`
3. `edges.csv` has the format: `source_id,target_id,weight`
4. The program must load these CSVs into an in-memory SQLite database.
5. You need to implement a query that matches a specific 3-node pattern. The exact pattern schema and filtering conditions are depicted in the image located at `/app/query_pattern.png`.
6. For every matching pattern, the query must compute a rolling sum of the edge weights partitioned by the target node's category, ordered by the source node's value. 
7. Print the results to standard output, with each row formatted exactly as: `<source_id>,<middle_id>,<target_id>,<rolling_sum>` ordered by `source_id` ascending, then `target_id` ascending.
8. The current query in the C file has an implicit cross join that causes duplicate paths and wrong rolling sums. Fix the SQL query to perform the correct explicit joins.
9. Add the necessary index creation statements (Index strategy design) in the C code before executing the main query to ensure optimal performance.
10. Compile your fixed C program to `/home/user/graph_analyzer` using `gcc -O3 graph_analyzer.c -lsqlite3 -o graph_analyzer`.

An automated fuzzer will test your `/home/user/graph_analyzer` binary against a reference implementation using various dynamically generated CSV datasets. Your output must exactly match the reference binary.