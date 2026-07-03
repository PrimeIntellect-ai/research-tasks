You are a database administrator tasked with optimizing a temporal graph query system. 

We have a video file located at `/app/graph.mp4`. This video encodes a temporal graph. Every frame in the video represents a single directed edge in the graph. 
To decode the edges, you must calculate the average color of each frame. Specifically, if you resize a frame to 1x1 pixel and extract its 8-bit RGB values:
- The Red channel (R) is the `source_node` (0-255).
- The Green channel (G) is the `target_node` (0-255).
- The Blue channel (B) is the `weight` of the edge (0-255).
- The frame number (starting at 1) represents the timestamp of the edge.

Your task is to:
1. Extract this data from `/app/graph.mp4` and load it into a new SQLite3 database located at `/home/user/graph.db`. Use the schema `edges(frame INTEGER, src INTEGER, dst INTEGER, weight INTEGER)`. 
2. Design and create appropriate indexes on the `edges` table to optimize temporal pathfinding queries.
3. Write a C program at `/home/user/query.c` and compile it to `/home/user/query`.
   - The program must accept exactly two command-line arguments: `start_node` and `end_node` (both integers).
   - It must connect to `/home/user/graph.db`.
   - It must use a parameterized SQL query featuring a Recursive Common Table Expression (CTE) to find the temporal shortest path from `start_node` to `end_node`. 
   - A valid temporal path is a sequence of edges where each subsequent edge has a strictly greater `frame` number than the previous one.
   - The "shortest" path is the one with the minimum sum of `weight`s. If there are ties, choose the path that arrives at `end_node` at the earliest `frame`.
   - The program should print exactly: `Weight: <total_weight>, Frames: <f1>,<f2>,...` followed by a newline. If no path exists, print `No path\n`.

Example output: `Weight: 142, Frames: 14,59,102`

You must use SQLite3 (`libsqlite3-dev` is installed). Ensure your query is highly optimized, as it will be evaluated against a large set of randomized node pairs to verify correctness and performance.