You are assisting a researcher who is organizing and reverse-engineering an archived social network dataset. 

An old, custom archiving pipeline encoded the network's edge list into a video file to save space, but the extraction script has been lost. The video is located at `/app/data_stream.mp4`. 

Here is what the researcher remembers about the video data model:
1. The video is exactly 100 frames long. Every frame consists of a single, uniform color.
2. Each frame represents exactly one directed edge in the graph.
3. The 8-bit RGB color values of the frame encode the edge data:
   - **Red channel (R):** Source Node ID (0-255)
   - **Green channel (G):** Target Node ID (0-255)
   - **Blue channel (B):** Edge Weight (0-255)

**Your Objectives:**
1. Extract the 100 edges from the video to reconstruct the directed graph. You can use any tools like `ffmpeg` or Python (e.g., `opencv-python` or `imageio`).
2. Write a Python script at `/home/user/query_graph.py` that processes this graph.

**Script Specifications:**
The script must accept exactly two positional command-line arguments (both integers):
`python3 /home/user/query_graph.py <start_node_id> <weight_limit>`

When executed, the script must:
1. Filter the entire extracted graph, keeping ONLY edges where `Weight <= weight_limit`.
2. Find the set of all nodes that are reachable from `<start_node_id>` via directed paths in this filtered graph (a node is always reachable from itself).
3. Determine the out-degree of every node *within this reachable set*, considering *only* the edges present in the filtered graph.
4. Output a strictly formatted JSON object to standard output containing:
   - `reachable_count`: The total number of reachable nodes.
   - `max_out_node`: The node ID in the reachable set with the highest out-degree (in the filtered graph). If there is a tie, return the node with the numerically lowest ID.

**Example Output:**
```json
{"reachable_count": 14, "max_out_node": 42}
```

The script must be highly reliable. An automated test suite will fuzz your script with dozens of random `<start_node_id>` and `<weight_limit>` pairs and assert that your output is bit-exact equivalent to a reference oracle.