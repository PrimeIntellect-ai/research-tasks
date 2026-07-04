You are a database administrator tasked with optimizing a slow graph database pipeline. Our application currently uses heavily nested Cypher queries to compute traversal paths, but it's proving too slow and complex for our real-time requirements. We are migrating the core traversal logic to a dedicated Rust worker.

In `/home/user/graph_data/`, you will find two files:
1. `schema_queries.cypher`: A log of the original Cypher `CREATE` and `MATCH` queries. You must reverse engineer this file to understand the implicit data model, node labels, and relationship properties.
2. `edges.csv`: A full data dump of the relationships. The columns are `source`, `target`, `cost`, and `state`.

Your task:
1. Analyze the Cypher file to understand which 'state' values represent traversable versus blocked paths.
2. Write a standalone Rust program at `/home/user/path_optimizer.rs`.
3. The Rust program must read `/home/user/graph_data/edges.csv`.
4. It must compute the shortest path (lowest total cost) from the node `"NODE_START"` to `"NODE_END"`. 
5. You must filter out any edges that have a state indicating they are blocked or deprecated (as deduced from the Cypher queries).
6. The program should output the IDs of the nodes in the shortest path, ordered from start to end, comma-separated, directly to a file named `/home/user/optimized_path.txt`.
7. Compile your script using `rustc /home/user/path_optimizer.rs` and run it to produce the output file.

Do not use any external crates; rely entirely on the Rust standard library for file reading, parsing, and graph traversal algorithms (e.g., Dijkstra's or BFS).