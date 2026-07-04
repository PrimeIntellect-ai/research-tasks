You are an expert Database Administrator and Data Engineer. 

A critical security incident has occurred, and you need to piece together a network intrusion graph by analyzing a combination of video surveillance metadata and raw database logs. 

We have provided a surveillance video file at `/app/surveillance.mp4`. The network rack's fault light flashes brightly at exact moments when malicious payloads were executed. You also have a raw network log file at `/app/network_logs.csv` containing the columns: `timestamp, src_ip, dst_ip, bytes`.

Your objective is to extract the timestamps of the flashes from the video, correlate them with the network logs, build a relational graph of the intrusion, and serve the results via an HTTP API written in Bash.

**Step 1: Video Extraction**
Analyze `/app/surveillance.mp4` using `ffmpeg` to detect the exact timestamps (in seconds) of scene changes or bright flashes (you can assume any frame with an average brightness > 0.8 or scene change score > 0.4 corresponds to a fault flash). 

**Step 2: Graph Database Construction**
Create a Bash script `/home/user/build_graph.sh` that:
1. Initializes an SQLite database at `/home/user/intrusion.db`.
2. Loads the `/app/network_logs.csv` data.
3. Flags any network connection in the database as `malicious` if its `timestamp` falls within ±1 second of any flash timestamp detected from the video.
4. Uses complex SQL joins (or CTEs) to model the network as a graph. You must identify all "Secondary Compromised Nodes" — defined as any `dst_ip` that received a connection from a `src_ip` that was involved in a `malicious` connection within the subsequent 10 seconds.

**Step 3: Multi-protocol API Server**
Create a Bash script `/home/user/serve_api.sh` that uses `socat` or `nc` to spawn a lightweight HTTP server listening on `127.0.0.1:8080`.
The server must respond to:
- `GET /api/v1/threats`
  Returns a strictly valid JSON response containing the compromised nodes.
  The JSON output schema must exactly match:
  ```json
  {
    "status": "success",
    "primary_malicious_edges": [{"src": "ip1", "dst": "ip2", "timestamp": 123.4}],
    "secondary_compromised_nodes": ["ip3", "ip4"]
  }
  ```

Run your server script in the background so it is listening for requests. Provide the necessary SQL query optimizations (like indexing the timestamp and ip columns) in your setup script to ensure the query executes in under 50ms.