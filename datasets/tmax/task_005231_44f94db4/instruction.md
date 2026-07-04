A researcher is organizing a dataset of entity interactions. The raw dataset is a screen recording `/app/dataset.mp4` that briefly flashes interaction events, one per frame.

You need to complete two objectives:

1. **Video Data Extraction**:
   Extract the interaction edges from the video `/app/dataset.mp4`. The video features a black background with white text. When an interaction occurs, the text displays two comma-separated alphanumeric node IDs (e.g., `NodeA,NodeB`), representing a directed edge from the first node to the second. 
   Extract these edges (use tools like `ffmpeg` and `tesseract` which are available). Clean up any OCR noise and save the unique edges to `/home/user/edges.txt`.

2. **Graph Aggregation Script**:
   Write a Bash script `/home/user/graph_builder.sh` that takes a file containing a list of edges (formatted like your `edges.txt`, one edge per line) as its first argument and outputs a normalized NoSQL-style JSON document representing the graph schema.
   
   The output must exactly match this format:
   ```json
   {
     "nodes": [
       {
         "id": "NodeA",
         "out_degree": 1,
         "targets": ["NodeB"]
       }
     ]
   }
   ```
   Rules for the JSON:
   - Only include nodes that have an out-degree > 0.
   - The `nodes` array must be sorted alphabetically by `id`.
   - The `targets` array for each node must contain unique neighbor IDs sorted alphabetically.
   - You must strictly use shell built-ins, standard coreutils (`awk`, `sed`, `grep`, `sort`, `jq`), and Bash logic.
   - Ensure the output is valid JSON (using `jq` to format is recommended).

3. **Final Integration**:
   Run your script on `/home/user/edges.txt` and save the output to `/home/user/video_graph.json`.

Ensure your script `/home/user/graph_builder.sh` is robust, as it will be tested against an extensive suite of random edge lists to verify strict functional equivalence to our reference implementation.