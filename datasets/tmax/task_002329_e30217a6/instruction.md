You are a data engineer building an ETL pipeline for an optical data-transmission system. The optical system outputs its network state as a video file, where each frame represents a slice of a temporal graph. You need to extract this data, materialize a flattened static graph, and build a fast query engine in C.

The video file is located at `/app/optical_graph.mp4`. 
- The video is exactly 128x128 pixels in resolution.
- It encodes an unweighted, directed graph where nodes are numbered 0 to 127.
- In each frame, the pixel at row `Y` (source node) and column `X` (destination node) indicates an edge if the grayscale intensity of that pixel is strictly greater than 128. 
- The final static graph is the union of all edges across all frames in the video.

Your task has two phases:

**Phase 1: Graph Materialization**
Write a C program (and/or bash scripts using `ffmpeg`) to extract the grayscale frames from `/app/optical_graph.mp4`. 
Project this data into a single, unioned 128x128 adjacency matrix. 
Export this matrix to a binary file at `/home/user/graph.bin`. The file must be exactly 16,384 bytes, where each byte represents the presence (1) or absence (0) of an edge at `[source][destination]` in row-major order.

**Phase 2: Query Engine**
Write and compile a C program located at `/home/user/query_engine`. 
This query engine must:
1. Accept exactly one command-line argument: the path to the materialized graph file (i.e., `/home/user/graph.bin`).
2. Read queries from standard input (`stdin`). Each line of `stdin` will contain a single integer `N`.
3. For each integer, calculate the total in-degree and out-degree for node `N` based on the materialized graph.
4. Output the result to `stdout` strictly in this format: `<N>|<in_degree>|<out_degree>` followed by a newline.
5. If `N` is less than 0 or greater than 127, print exactly `ERROR` followed by a newline.
6. Process inputs continuously until `EOF`.

You must fully complete both phases. Leave the compiled executable at `/home/user/query_engine` and the materialized graph at `/home/user/graph.bin` when you are finished.