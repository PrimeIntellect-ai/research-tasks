You are a database administrator tasked with optimizing and restoring a graph query pipeline for a legacy system. 

We have partially lost the schema and edge data for our internal knowledge graph. However, we managed to recover a database file and a screen recording.
1. The nodes of the graph are stored in a local SQLite database at `/app/legacy_nodes.db` (table: `nodes`, columns: `id`, `label`).
2. The edges were lost from the database, but we have a screen recording of the legacy edge list in `/app/schema_edges.mp4`. The video is exactly 10 seconds long (30 FPS). Every 1 second (starting from 0.0, i.e., frames 0, 30, 60...), a single text overlay appears in the center of the video in the format `SRC_LABEL->DST_LABEL` (e.g., `ALPHA->BETA`). The text is large, white, and clearly visible. 

Your task:
1. Reverse engineer the data model and extract the missing edge data from `/app/schema_edges.mp4`. You may use `ffmpeg` and OCR tools (like `tesseract`) to parse the frames.
2. Reconstruct the full knowledge graph (you can materialize it into a new database or hold it in memory).
3. Write a Python script at `/home/user/project_graph.py` that takes two command-line arguments: `node_label` and `max_depth`.
4. The script must perform graph projection/pattern matching to find all unique node labels reachable from `node_label` within `max_depth` directed hops. 
5. The script must print the resulting labels (including the source `node_label`) to standard output as a comma-separated list sorted in alphabetical order.

Example invocation:
`python3 /home/user/project_graph.py ALPHA 2`
Expected output format:
`ALPHA,BETA,DELTA,GAMMA`

Ensure your script is robust and highly optimized for repeated queries, as it will be heavily tested against an oracle with random inputs.