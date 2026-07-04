You are an AI assistant helping a researcher organize and query a dataset of network routes.

We have a video file located at `/app/network_scans.mp4`. This video is a sequence of frames, each containing a QR code. Every QR code encodes a single directed edge of our network graph in the text format:
`SourceNode,DestinationNode,Weight`
(e.g., `42,105,8`)

Your task is to:
1. Extract all the frames from the video and decode the QR codes (the `zbarimg` utility is available) to reconstruct the complete dataset of graph edges. Consolidate these into a file.
2. Reverse engineer the bounds of the data model (identifying the max node ID to design your memory/index strategy). 
3. Write a C program at `/home/user/graph_query.c` that loads this extracted edge dataset, builds an efficient graph index (like an adjacency list), and answers shortest-path queries.
4. Compile your program to `/home/user/graph_query`.

The C program requirements:
- It must read the graph edges from the file you created (hardcode the path to the consolidated edge file in your C code, or read it at startup, but it must not require the path as a command-line argument).
- After loading the graph, it must read parameterized queries from `stdin`. Each line of `stdin` will contain two integers separated by a space: `Source Target`.
- For each query, compute the shortest path distance from `Source` to `Target` using Dijkstra's algorithm.
- Print the integer total weight of the shortest path to `stdout` followed by a newline. If the target is unreachable from the source, print `-1`.
- The program should process queries until `EOF` on `stdin`.

Ensure your C code is optimized for multiple sequential queries on the same graph structure. Do not print any extraneous text or prompts to `stdout`—only the integers representing the shortest path distances.