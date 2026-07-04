You are a data analyst tasked with recovering and analyzing network graph data that was mistakenly encoded into a video format.

A video file is located at `/app/graph_evolution.mp4`. The video is exactly 10 seconds long, encoded at 1 Frame Per Second (10 frames total). 
Each frame contains a 100x100 pixel image that represents an adjacency matrix of a directed graph with 10 nodes (labeled 0 through 9).
The image is a 10x10 grid of blocks, where each block is 10x10 pixels. 
- Row `i`, Column `j` (where Row 0 is top and Col 0 is left) is solid BLACK (RGB 0,0,0) if an edge exists from node `i` to node `j` in that frame.
- It is solid WHITE (RGB 255,255,255) if no edge exists.

Your task is to:
1. Extract the adjacency matrix from each frame of the video. 
2. Create an intermediate CSV file `edges.csv` containing every edge found across all frames. The schema must exactly match: `frame_index,source,target` (no spaces).
3. Write a C++ program `/home/user/aggregate.cpp` that reads `edges.csv`, validates the schema, and acts as an aggregation pipeline. The C++ program should materialize an aggregated graph where the weight of an edge `(i, j)` is the count of frames in which it appeared.
4. The C++ program must project this graph into a final output CSV named `/home/user/node_stats.csv`. The schema for this file must be: `node,total_out_weight,total_in_weight`. It must contain exactly 10 data rows (for nodes 0 to 9), sorted by `node` in ascending order.

You may use standard CLI tools (like `ffmpeg`, `imagemagick`, `awk`, etc.) or write helper scripts to parse the video. However, the aggregation, schema validation, and graph projection MUST be implemented in C++ and compiled with `g++`.

Ensure your final output file `/home/user/node_stats.csv` is correctly formatted.