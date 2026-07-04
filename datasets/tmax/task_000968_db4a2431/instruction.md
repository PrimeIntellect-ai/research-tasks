You are a data analyst investigating a compromised sensor network. You have two pieces of evidence:
1. A raw network topology log: `/app/network_topology.csv`
2. A surveillance video from the server room: `/app/signal_log.mp4`

The CSV contains potential network edges with the following schema:
`timestamp_sec,source_node,target_node,latency_ms`

However, not all edges in the CSV were actually active. An edge is only considered "active" if the server room's surveillance video indicates a high-activity signal at that exact second. Specifically, you must analyze the video using `ffmpeg`'s `signalstats` filter. An edge is active ONLY if the average luma (`YAVG`) of the video frame at `timestamp_sec` is strictly greater than 100.

Your objective is to:
1. Pre-process the video and CSV to filter out inactive edges. 
2. Write a C++ program that loads the active network graph.
3. The C++ program must read queries from `stdin`. Each query will be a line containing two integers: `Start_Node End_Node`.
4. For each query, compute the shortest path (minimum total `latency_ms`) between the two nodes using Dijkstra's algorithm. If a path exists, output the total latency. If no path exists, output `-1`.
5. Write a shell script at `/home/user/query_solver.sh` that compiles your C++ program (if not already compiled) and executes it, passing `stdin` directly to your C++ binary.

Requirements:
- Your C++ program must be optimized to handle up to 10,000 queries efficiently.
- Do not hardcode the CSV parsing; it must dynamically read the filtered data.
- The output must be exactly one integer per line, corresponding to the shortest path cost for each query.
- Use standard `ffmpeg` tools for frame analysis.