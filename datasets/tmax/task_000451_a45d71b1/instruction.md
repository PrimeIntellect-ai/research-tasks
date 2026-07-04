Hello, I am a compliance officer conducting a post-incident audit. We have reason to believe an external breach occurred, but the system logs were corrupted by the attacker. However, a secure terminal managed to record the access events as a video stream of QR codes before going offline. 

I need you to recover the audit trail and perform a graph-based impact analysis. 

Here is what you need to do:
1. **Extract and Decode**: Process the video file located at `/app/audit_stream.mp4`. Each frame containing a valid QR code encodes a JSON string representing a system access event. The JSON format is `{"src": "<Node_ID>", "dst": "<Node_ID>", "ts": <timestamp>, "action": "<action_type>"}`. 
2. **Build and Project the Graph**: Construct a directed graph from these events. We are only interested in tracing lateral movement. An access path is only valid if it is time-ordered (i.e., for an edge A->B at $t_1$ and B->C at $t_2$, $t_1 \le t_2$).
3. **Query Pipeline**: 
    - The initial breach originated from the node `IP_EXT_994`. 
    - Chain queries to find all downstream `System_*` nodes that could have been reached from `IP_EXT_994` through valid time-ordered paths.
    - Calculate a "vulnerability score" for each reachable system, defined as the number of unique time-ordered paths from the breached node to that system.
4. **Pagination and Filtering**: Sort the systems in descending order of their vulnerability score, and alphabetically by Node_ID in case of a tie. Filter out any nodes that are not systems (only include nodes starting with `System_`). Retrieve the top 50 most vulnerable systems.

**Output:**
Create a CSV file at `/home/user/vulnerable_systems.csv` with exactly two columns: `system_id` and `vulnerability_score`. The file must contain exactly 50 rows of data (plus a header row).

You may use any tools or languages you prefer. You will likely need to install dependencies for video processing and QR code decoding (e.g., `ffmpeg`, `pyzbar`, `opencv-python`).