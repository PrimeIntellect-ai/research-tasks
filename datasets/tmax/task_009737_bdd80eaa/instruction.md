You are a data engineer working on an ETL pipeline that migrates hierarchical data from a legacy relational database to a modern NoSQL document store.

You have been provided with an export of the relational data representing a category tree (an adjacency list graph) in a CSV file located at `/home/user/input_graph.csv`. 

The CSV format is:
`node_id,parent_id,node_name`
(Note: `parent_id` is `0` if the node is a root node).

Your task is to write a C program that loads this relational graph, resolves the full hierarchical path for each node from the root to the node itself (a recursive/hierarchical operation), and maps it into a document-oriented representation. 

Specifically, you need to write and compile a C program at `/home/user/build_paths.c`. When run, the compiled executable `/home/user/build_paths` must generate a JSON Lines file at `/home/user/output_docs.jsonl`.

Each line in the JSONL output must be a valid JSON object representing one node, formatted exactly like this (without extra spaces around keys/values, except for standard JSON formatting):
`{"id": 3, "name": "Laptops", "path": ["Electronics", "Computers", "Laptops"]}`

Requirements for the C program:
1. Parse the CSV file `/home/user/input_graph.csv` (you may assume a maximum of 100 nodes and maximum line length of 256 characters).
2. Store the nodes in an appropriate internal struct array to represent the schema and relationships.
3. Compute the path recursively for each node.
4. Output the cross-representation mapping as strict JSON Lines to `/home/user/output_docs.jsonl`. Ensure the `id` is an integer, and `name` and items in `path` are strings. The order of output lines must be sorted by `id` in ascending order (1, 2, 3...).

Complete the ETL job by writing the C code, compiling it with `gcc`, and executing it to produce the final `output_docs.jsonl` file.