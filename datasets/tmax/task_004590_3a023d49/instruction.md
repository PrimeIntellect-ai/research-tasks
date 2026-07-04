You are a data engineer building an ETL pipeline that reconstructs a NoSQL database schema from legacy video archives and processes incoming hierarchical updates.

We have an archived video at `/app/schema_stream.mp4`. This video is a screen recording that flashes QR codes, each containing a JSON snippet representing a piece of our base NoSQL schema (parent-child relationships). 

Your task involves two phases:

**Phase 1: Base Graph Extraction**
1. Use `ffmpeg` to extract frames from `/app/schema_stream.mp4` (extracting at 1 frame per second is sufficient).
2. Use a tool like `zbarimg` to decode the QR codes in these frames.
3. Combine the decoded JSON snippets into a single base dictionary mapping each `parent_node` to a list of its `child_nodes`. The root of this base graph is always exactly the string `"ROOT"`.

**Phase 2: ETL Processing Script**
Write a Python script at `/home/user/etl_graph.py`. This script must act as a stream processor that does the following:
1. Hardcode or dynamically load the base graph you extracted in Phase 1.
2. Read a JSON array from standard input (`stdin`). This array contains new NoSQL-like document edges, e.g., `[{"source": "node_A", "target": "node_B"}, ...]`.
3. Merge these new edges into the base graph.
4. Perform a recursive/hierarchical query starting from `"ROOT"` to find all leaf nodes (nodes with no children).
5. For every leaf node, calculate its exact depth from `"ROOT"` (where `"ROOT"` is depth 0).
6. Output a JSON object mapping each leaf node to its depth, sorted alphabetically by the leaf node's name, e.g., `{"leaf_A": 3, "leaf_B": 2}`.

Your script must be robust, executable (`chmod +x`), and correctly handle arbitrary additional edges provided via standard input.