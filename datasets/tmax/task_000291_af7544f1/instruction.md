You are a data engineer building an ETL pipeline to process a custom graph dataset. We need a C program to perform a specific graph traversal query, essentially executing a hard-coded query plan to extract relationship paths.

Your task is to write a C program located at `/home/user/graph_etl.c` that reads two CSV files representing a graph:
1. `/home/user/nodes.csv`: Contains node definitions with columns `id,type`.
2. `/home/user/edges.csv`: Contains directed edge definitions with columns `source_id,target_id,relation`.

The program must find all paths matching the following Cypher-like pattern:
`(u:User)-[:BUYS]->(o:Order)-[:CONTAINS]->(p:Product)`

For every match found, the program must output the user ID and the product ID to `/home/user/results.csv` in the format `user_id,product_id`.
The output file must be sorted numerically by `user_id` in ascending order, and then by `product_id` in ascending order. Do not include a header in the output file.

Compile your program to `/home/user/graph_etl` and run it to generate the `results.csv` file. 

Assumptions:
- IDs are positive integers.
- Max line length in CSVs is 256 characters.
- There are at most 10,000 nodes and 10,000 edges.
- Use standard C libraries.
- `nodes.csv` and `edges.csv` will be present in `/home/user/` when your program runs.