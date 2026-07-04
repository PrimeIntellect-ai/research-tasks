You are a Database Reliability Engineer (DBRE) tasked with recovering a corrupted backup replication topology. The topology configuration was lost, but a diagnostic video log containing the replication edges has been recovered.

Your task is to write a C program that recovers this topology, computes optimal backup restoration paths, and serves them via an HTTP API.

Step 1: Extract the Topology from Video
A video artefact is located at `/app/backup_topology.mp4`. 
- The video consists of exactly 50 frames (at 1 fps).
- Each frame represents a single directed replication edge between two storage nodes.
- To decode an edge from a frame, look at the RGB color of the top-left pixel (x=0, y=0):
  - Red channel (0-255): Source Node ID
  - Green channel (0-255): Destination Node ID
  - Blue channel (0-255): Replication Latency (Edge weight)

Step 2: Build the Shortest Path Server in C
Write a C program that:
1. Parses the extracted frame data to build a directed graph in memory.
2. Starts an HTTP web server listening on `127.0.0.1:8080`.
3. Handles `GET /restore_path?source=<ID>&dest=<ID>` requests.
4. Uses Dijkstra's algorithm (or another shortest-path graph traversal algorithm) to find the path with the minimum total latency from the source node to the destination node.
5. Responds with HTTP 200 OK and a JSON payload in this exact format:
   `{"path": [10, 15, 42], "total_latency": 120}`
   If no path exists, return `{"error": "no path"}` with a 404 status.

Constraints & Tips:
- You may use `ffmpeg` to extract the frames from the video into a raw format (e.g., `.ppm` or raw RGB) to easily parse them in your C program.
- You must write the HTTP server and graph traversal logic in C from scratch (using standard POSIX sockets). Do not use external web frameworks.
- The system has `gcc`, `make`, and `ffmpeg` pre-installed.
- Run your C server in the background once compiled.