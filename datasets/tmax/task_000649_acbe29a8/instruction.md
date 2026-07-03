You are a data analyst managing a logistics network. We have an automated system that monitors disruptions, but its logs have been corrupted. The only surviving record of the network state is a diagnostic video feed.

Your task is to rebuild the network state by analyzing this video, fuse it with the static network topology, and deploy a high-performance C-based query service to serve pathfinding requests.

**Phase 1: Video Data Extraction**
1. An MP4 video is located at `/app/network_status.mp4`. The video is exactly 30 seconds long, encoded at 1 frame per second (30 frames total, indexed 0 to 29).
2. The video resolution is 100x100 pixels. The frame is divided into a 10x10 grid of cells (each cell is 10x10 pixels).
3. The background is pure black `(0,0,0)`. In each frame, exactly one cell is highlighted in pure red `(255,0,0)`.
4. This red cell indicates the "Target Node" for that specific second (frame). Nodes are numbered 0 to 99. The node ID is calculated by its grid position: `Node_ID = (X_coordinate / 10) + (Y_coordinate / 10) * 10`.
5. You must extract this Target Node for each frame. You may use `ffmpeg` and scripting languages (like Python) for this extraction phase. Output your findings into a local CSV named `active_nodes.csv` (format: `frame_id,node_id`).

**Phase 2: Graph Construction and Query Server in C**
1. The static network topology is provided in `/app/network_graph.csv` (format: `source,destination,weight`). The graph is undirected.
2. Write a C program that:
   - Reads `/app/network_graph.csv` into memory as a graph data structure.
   - Reads your generated `active_nodes.csv`.
   - Starts a TCP server listening on `127.0.0.1:8888`.
3. The server must handle incoming TCP connections with the following protocol:
   - A client connects and sends a query in the exact format: `QUERY <frame_id>\n` (e.g., `QUERY 5\n`).
   - The server must compute the shortest path cost (using Dijkstra's algorithm or similar) from the static origin **Node 0** to the Target Node corresponding to that `frame_id`.
   - The server must reply exactly with: `PATH_COST: <cost>\n` (e.g., `PATH_COST: 45\n`). If a node is unreachable, the cost should be `-1`.
   - The server should keep the connection open for multiple queries until the client disconnects, and gracefully handle multiple sequential clients.

Compile your C program, run it in the background, and ensure the port is actively listening before you finish.