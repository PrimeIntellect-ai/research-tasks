You are tasked with recovering and analyzing network interaction data. We have a video recording of a network monitoring dashboard (`/app/network_traffic.mp4`) and an SQLite database (`/app/network.db`) containing historical event logs.

Unfortunately, the database suffered a partial corruption. The `event_logs` table has a corrupted index on the `event_time` column, which causes standard `SELECT` queries filtering by `event_time` to return stale, duplicate, or missing rows if the index is used. 

Your objectives are:
1. **Video Analysis:** The video (`/app/network_traffic.mp4`, 30 FPS) contains a small indicator box in the top-left corner (from pixel x:0-50, y:0-50) that flashes pure white `(255, 255, 255)` when a critical network anomaly occurs. Analyze the video to find the exact frame numbers of these flashes. Calculate the timestamp of each flash as `frame_number / 30.0`.
2. **Database querying and repair:** Write a Python script to query the `/app/network.db` SQLite database. You must find all `event_logs` where the `timestamp` is within 0.1 seconds of any anomaly timestamp detected in the video. **Crucially**, you must work around or fix the corrupted index on `event_time` to ensure you get accurate, non-duplicate rows.
3. **Graph Analysis:** The `event_logs` table contains `source_node` and `target_node` columns, and a `payload_size` column. Using the anomalies you correlated, construct a directed graph where edges are the anomalies, and the edge weight is `payload_size`.
4. **Result Calculation:** Compute the shortest path distance (minimum total payload size) from node `'NODE_A'` to `'NODE_Z'` in this anomaly graph.
5. **Output:** Save the calculated shortest path distance as a single float/integer in `/home/user/result.txt`.

Ensure your Python code runs efficiently and correctly processes the video and the database joins.