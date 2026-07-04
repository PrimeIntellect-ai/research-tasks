You are an AI assistant helping a data researcher organize and analyze a complex urban logistics dataset. The researcher has provided a video feed from a traffic drone and a set of user-submitted graph queries that need sanitizing. You must complete a multi-stage workflow using Rust, PostgreSQL, and ffmpeg.

**Stage 1: Video-Derived Edge Weights**
You are provided with a video file at `/app/drone_feed.mp4`. This video records traffic congestion. Specifically, at certain frames, the screen flashes purely red (where average pixel color has R > 200, G < 50, B < 50). 
1. Use `ffmpeg` and any necessary scripting to analyze `/app/drone_feed.mp4` and identify the exact frame numbers of these red flashes.
2. The dataset has 100 sequential edges. The number of red flashes found within the video determines the base congestion multiplier. Calculate `congestion_multiplier = (Total Red Frames) * 1.5`.

**Stage 2: Database Initialization and Indexing**
1. Start a local PostgreSQL instance (you can use Docker or local services). 
2. Create a database named `logistics`.
3. Create a table `routes` with columns: `edge_id (INT)`, `source_node (VARCHAR)`, `target_node (VARCHAR)`, `base_cost (FLOAT)`.
4. Load the dataset from `/app/raw_routes.csv` into the `routes` table.
5. Design and apply an optimal index strategy on the `routes` table to support extremely fast pathfinding queries based on `source_node` and `target_node`.
6. Write a Rust program at `/home/user/graph_builder/` that connects to PostgreSQL, reads the `routes`, and updates all `base_cost` values by multiplying them by your calculated `congestion_multiplier`. You MUST use parameterized queries for the update operations.

**Stage 3: Graph Analytics and Export**
Extend your Rust program to:
1. Load the updated edges into an in-memory graph structure.
2. Compute the shortest path from node "DEPOT_ALPHA" to "DISTRIBUTION_ZETA".
3. Compute the degree centrality of all nodes.
4. Export the shortest path (as an ordered array of node IDs) and the top 5 most central nodes to `/home/user/graph_results.json` in the following format:
```json
{
  "shortest_path": ["DEPOT_ALPHA", "NODE_X", ..., "DISTRIBUTION_ZETA"],
  "top_centrality": [
    {"node": "NODE_Y", "degree": 45},
    ...
  ]
}
```

**Stage 4: Query Sanitizer (Adversarial Corpus)**
The researcher allows community analysts to submit JSON-based filtering queries to run against the graph dataset. However, malicious users try to inject destructive SQL commands or path traversal commands via the JSON parameters.
1. Write a Rust CLI application at `/home/user/sanitizer/` that takes a single file path as a command-line argument.
2. The application must read the JSON file, inspect the `"query_filter"` field, and determine if it is safe or malicious.
3. If safe, exit with code 0. If malicious (contains SQL injection attempts like `DROP TABLE`, `1=1`, or path traversal like `../`), exit with code 1.
4. Your sanitizer must successfully classify the clean and evil corpora provided by the researcher.

Ensure your Rust code compiles and all dependencies are correctly managed in your `Cargo.toml`. You may use any standard community crates (e.g., `postgres`, `sqlx`, `serde`, `petgraph`).