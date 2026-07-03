You are a Database Administrator and Performance Engineer working on a custom, in-memory Knowledge Graph engine written in Rust. 

Your team has a Rust project located at `/home/user/kg_engine` that reads a large knowledge graph from a CSV file (`/home/user/data/edges.csv`) and executes a specific pattern-matching query. The graph represents directed relationships between entities.

The current query seeks to identify all "Influence Clusters"—defined strictly as **Directed Triangles** (Node A -> Node B -> Node C -> Node A). After finding all unique nodes that participate in at least one Directed Triangle, the engine must calculate the out-degree centrality (total number of outgoing edges in the *entire* graph) for those specific nodes, and output the top 5 nodes with the highest out-degree.

**The Problem:**
The original developer wrote the pattern matching as a naive nested loop over the edge list (effectively a poorly planned O(E³) relational join). On the production dataset, this query plan takes way too long to execute. 

**Your Task:**
1. Navigate to `/home/user/kg_engine`.
2. Modify `src/main.rs` to optimize the query execution plan. You should replace the naive nested loop approach with an efficient graph traversal or indexed join strategy (e.g., building adjacency lists/hash maps to act as indexes for O(1) lookups).
3. Ensure the program correctly identifies all unique nodes involved in Directed Triangles.
4. For those identified nodes, calculate their out-degree centrality based on the *entire* graph.
5. Sort these nodes by out-degree descending. In case of a tie, sort by Node ID ascending.
6. Write the top 5 Node IDs as a plain JSON array of integers to `/home/user/results.json`.
7. Your Rust program must compile with `cargo build --release` and execute the entire pipeline (reading, querying, calculating, and writing the JSON) in under 2 seconds.

**Environment Details:**
- The graph edges are provided in `/home/user/data/edges.csv` (headers: `source,target`).
- You may use standard Rust library features and the existing dependencies in `Cargo.toml`. You are permitted to add standard crates like `serde`, `serde_json`, or `csv` if needed, but you must write the optimized graph pattern matching logic yourself.
- Execute your optimized Rust program to produce the final `/home/user/results.json` file.