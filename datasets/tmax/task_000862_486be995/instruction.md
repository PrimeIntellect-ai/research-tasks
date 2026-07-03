You are a database administrator tasked with optimizing a critical data processing pipeline. We have a legacy proprietary graph query engine provided as a stripped binary at `/app/legacy_engine`. This engine is currently used to perform complex knowledge graph pattern matching, result filtering, sorting, and pagination over large datasets, but it is too slow and we lost the source code.

Your objective is to reverse-engineer the query execution plan and exact filtering/sorting logic of `/app/legacy_engine` and write a high-performance equivalent in C++.

The legacy engine is invoked from the command line as follows:
`/app/legacy_engine <path_to_edges.csv> <path_to_nodes.csv> <offset> <limit>`

The inputs are formatted as follows:
- `nodes.csv`: `node_id,node_type,weight` (where node_id is an integer, node_type is a string, and weight is a float).
- `edges.csv`: `source_id,target_id,relationship_type` (where source/target are integers, and relationship_type is a string).
- `offset` and `limit` are integers used for pagination of the final result set.

The output is written directly to standard output as a CSV with a header, representing the sorted and paginated results of a specific graph pattern query.

Your task:
1. Analyze the behavior of `/app/legacy_engine` using standard Linux tools (you may create dummy CSV files to test its outputs).
2. Deduce the exact knowledge graph pattern it matches (e.g., specific paths, triangles, or structural queries), including any implicit subqueries, filtering conditions on weights or types, and the exact multi-column sorting strategy.
3. Write a C++ program at `/home/user/query_engine.cpp` that perfectly replicates this logic.
4. Compile your program to `/home/user/query_engine`. It must accept the exact same command-line arguments and produce bit-exact identical standard output as the legacy engine for any valid input graph. 

The C++ code must implement efficient index strategy design internally (e.g., adjacency lists, hash maps for node lookups) to ensure it can handle large graphs without timing out.