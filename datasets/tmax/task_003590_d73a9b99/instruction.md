I need you to help me with a two-part data processing pipeline involving video analysis and building a Rust-based graph projection tool.

**Part 1: Video Scene Analysis**
I have a video file located at `/app/scene.mp4`. I need you to analyze this video to detect scene changes. Please use `ffmpeg` to find all frames where the scene change detection score is strictly greater than `0.4` (using the `select='gt(scene,0.4)'` filter). 
Count the exact number of these scene change frames and write this single integer to `/home/user/scene_changes.txt`.

**Part 2: CSV Graph Projector (Rust)**
I am working with tracking data from these videos, exported as CSVs. I need you to create a Rust CLI tool that processes this CSV data into a graph, calculates connected components, and exports the result.

Create a new Rust project at `/home/user/graph_projector`.
The tool must read CSV data from `stdin` (no header row). The columns are:
`source_id (u32)`, `target_id (u32)`, `interaction_weight (f64)`, `frame_id (u32)`

Your Rust program needs to perform the following pipeline:
1. **Filter**: Only consider rows where `interaction_weight > 0.5`.
2. **Project and Materialize**: Build an undirected graph from the filtered rows. Nodes are the IDs. An edge exists between `source_id` and `target_id`. If multiple rows exist for the same pair of nodes (regardless of order, as it's undirected), their edge weights should be aggregated by summing the `interaction_weight`s. 
3. **Query**: Find all connected components in this undirected graph. Isolated nodes (nodes that appeared in the CSV but had no edges after filtering) should be treated as components of size 1.
4. **Export**: Output the connected components to `stdout` as a JSON array of arrays of integers. 
   - Each inner array represents a connected component and must be sorted in ascending order.
   - The outer array must be sorted descending by the size of the component. If two components have the same size, break ties by sorting them ascending based on the smallest node ID in the component.

*Example Input:*
```csv
1,2,0.6,10
2,3,0.2,11
4,5,0.8,12
2,1,0.7,13
```
*Example Output:*
```json
[[1,2],[4,5],[3]]
```

Requirements for the Rust tool:
- The compiled binary must be available at `/home/user/graph_projector/target/release/graph_projector`.
- Use `cargo build --release` to compile it.
- It should fail gracefully or ignore malformed lines, but you can assume the test inputs will be well-formed CSVs.
- Do not print anything else to `stdout` except the final JSON array.