You are a data engineer tasked with building an ETL pipeline that extracts network topology from a video recording and provides a query interface for hierarchical graph analytics.

We have a video artefact at `/app/network_traffic.mp4`. This video contains a screen recording of a dashboard, but more importantly, it has an embedded subtitle track (stream 0:s:0) that logs routing events over time. 

Your tasks are as follows:

**Phase 1: Data Extraction**
Extract the embedded subtitle track from `/app/network_traffic.mp4` (you may use `ffmpeg`, which is preinstalled). The subtitles contain text in the following exact format:
`Route: [Source_ID] -> [Target_ID] | Bytes: [Integer]`
For example: `Route: Xray_9 -> Delta_2 | Bytes: 4050`

Parse these events and load them into a SQLite database at `/home/user/network.db` in a table named `edges` with columns `source`, `target`, and `bytes`. If there are multiple edges between the same source and target in the video, sum their bytes into a single edge in the database.

**Phase 2: Graph Analytics Program**
Write a Python script at `/home/user/query_network.py` that takes a single string argument (a Node ID, like `Xray_9`). The script must connect to `/home/user/network.db` and output a single JSON-encoded dictionary to stdout.

The script must compute the following using a **single SQL query** (utilizing Recursive CTEs and Window Functions):
1. Traverse the network downstream (directed from source to target) starting from the provided Node ID. The start node is at `level 0`, its immediate targets are at `level 1`, and so on. (Assume no cycles in the downstream path for a given node).
2. For every descendant node discovered, identify its hierarchical level. If a node is reachable via multiple paths, use the minimum level (shortest path).
3. Use a window function to find the maximum `bytes` edge that points *to* any node within each level (for level 0, the max bytes is 0).

The output must be strictly a single JSON string with this format:
```json
{
  "start_node": "Xray_9",
  "total_descendant_bytes": 15000,
  "max_bytes_per_level": {
    "1": 4050,
    "2": 8200
  }
}
```
*Note:* `total_descendant_bytes` is the sum of `bytes` of all edges traversed in the directed subgraph rooted at the start node. `max_bytes_per_level` contains string keys representing the level integer, and values representing the highest single edge `bytes` terminating at a node of that level.

Requirements:
- Your Python script must use standard libraries (like `sqlite3`, `json`, `sys`, `argparse`).
- Make sure `/home/user/query_network.py` has executable permissions.