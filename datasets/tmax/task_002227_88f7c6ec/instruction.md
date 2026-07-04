You are an expert Database Administrator. We are recovering a legacy query system. We have a visual query execution log, but the original query planner is corrupted. You need to analyze the execution log video and write a highly optimized Python script to act as a fallback graph query engine.

Phase 1: Video Analysis
A legacy monitoring tool generated an execution visualization video located at `/app/query_viz.mp4`. 
The video represents database transactions. Most frames are black, but a frame turns completely green (RGB value exactly `0, 255, 0`) every time a high-priority commit occurs. 
Analyze the video to count the exact number of completely green frames. Let this number be `N`. You may use `ffmpeg` or Python with `opencv-python` to extract and analyze the frames.

Phase 2: Graph Query Script
You must write an optimized Python script at `/home/user/graph_query.py`.
This script will be tested heavily against a reference implementation using thousands of random graphs to ensure perfect functional equivalence and high performance.

Requirements for `/home/user/graph_query.py`:
1. It must read a single line of JSON from `sys.stdin`.
2. The JSON represents a knowledge graph with the following structure:
   `{"nodes": [{"id": "str", "type": "str", "price": int_optional}, ...], "edges": [{"source": "id1", "target": "id2"}, ...]}`
3. Implement a graph pattern matching algorithm to find all nodes of `type` == `"User"`.
4. A "User" node qualifies if it is connected (either as a source or target in an edge) to AT LEAST one node of `type` == `"Product"` where the product's `price` is strictly greater than `N` (the count from Phase 1).
5. Extract the `id`s of all qualifying User nodes.
6. Sort the extracted User `id`s in descending alphabetical order.
7. Apply pagination/limiting: take only the first 5 IDs from the sorted list.
8. Print the final IDs as a comma-separated string to `sys.stdout` (e.g., `user7,user3,user1`). If none match, print nothing (just a newline).
9. You must design an index strategy (e.g., building adjacency lists and type dictionaries in memory) to ensure the query runs efficiently even on graphs with 100,000+ nodes and edges.

Ensure your script processes standard input correctly and handles missing `price` fields gracefully (only "Product" nodes will have a price). Do not include any debug output in your final script.