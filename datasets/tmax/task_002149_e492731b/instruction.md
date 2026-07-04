You are a database administrator troubleshooting a custom in-memory graph querying tool written in C. The tool is designed to find 2-hop paths (A -> B -> C) between specific types of nodes in a network. 

However, the current implementation is producing massive amounts of incorrect output because of a logical flaw: it performs an implicit cross-join on the edges array rather than properly traversing connected edges (it doesn't ensure the target of the first edge is the source of the second edge). It also lacks filtering and pagination capabilities.

Your task:
1. Review the C source code located at `/home/user/find_paths.c`, alongside the graph data in `/home/user/nodes.csv` and `/home/user/edges.csv`.
2. Fix the implicit cross-join bug in `/home/user/find_paths.c` so it only finds valid 2-hop paths (where `edge1.target_id == edge2.source_id`).
3. Modify the program to accept three command-line arguments: `<start_node_type> <end_node_type> <limit>`. The program should filter paths such that node A matches `<start_node_type>` and node C matches `<end_node_type>`.
4. Ensure the program sorts the valid paths alphabetically by the resulting string representation `"A_name -> B_name -> C_name"` and prints only up to `<limit>` results.
5. Compile the fixed C program to `/home/user/find_paths`.
6. Run your compiled program to find paths from `User` to `Product` with a limit of `5`. Save the exact standard output to `/home/user/results.txt`.

Data schema:
- `nodes.csv`: `id,type,name`
- `edges.csv`: `source_id,target_id,relation_type`

Output format for `results.txt`:
```
[Node A Name] -> [Node B Name] -> [Node C Name]
...
```