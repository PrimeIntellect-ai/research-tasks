You are a Database Reliability Engineer investigating the backup replication topology of our distributed database cluster. 

We lost our topology documentation during a recent incident, but we managed to recover a dashboard recording at `/app/backup_topology.mp4`. The video is 3 seconds long (1 frame per second). In each frame, the dashboard displayed a QR code containing a JSON fragment of the network schema, specifically the backup replication links and their latencies.

Your task is to:
1. Extract the frames from `/app/backup_topology.mp4` and decode the QR codes. You can use standard tools like `ffmpeg` and `zbarimg` to read the codes.
2. Reconstruct the full undirected graph of the backup topology from the extracted JSON fragments.
3. Write a C++ service that acts as a query server to analyze the topology. The C++ code must be saved to `/home/user/topology_server.cpp` and compiled to `/home/user/topology_server`.
4. The C++ service must listen for incoming plain-text TCP connections on `127.0.0.1:8080`.

The TCP service must support the following newline-terminated text commands:
- `PATH <src> <dst>`: Calculates the shortest path between the two nodes based on latency. It must respond with the comma-separated path nodes and the total latency, separated by a space, followed by a newline. (Example response: `db1,db2,db5 35\n`)
- `DEGREE <node>`: Calculates the degree centrality (number of connected edges) of the specified node. It must respond with the integer degree followed by a newline. (Example response: `3\n`)

Constraints & Details:
- The graph is undirected.
- Start the server in the background once compiled.
- Ensure the server stays running and can handle multiple sequential requests from clients (like `netcat`).
- Do not output anything to the client other than the exact expected responses.

You have all standard Linux shell tools, `ffmpeg`, `zbar-tools`, and `g++` available.