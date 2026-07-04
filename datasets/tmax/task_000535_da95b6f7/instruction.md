You are an operations engineer triaging a bizarre incident that occurred during a robotic deployment. We have a video feed of the incident (`/app/incident.mp4`) and a telemetry database (`/home/user/telemetry.db`).

Your colleague wrote a Bash pipeline (`/home/user/triage.sh`) and an API server script (`/home/user/server.sh`) to analyze the video, correlate it with the database, and serve the results to our incident response dashboard. However, the pipeline is currently broken due to several subtle bugs:

1. **Floating-Point Precision:** The script uses standard `awk` float arithmetic to sum frame durations. Due to floating-point accumulation errors, it misidentifies the critical timestamp.
2. **Boundary/Off-by-One:** Frame indices are 0-indexed in our database, but the script miscalculates the index when correlating the extracted video frames.
3. **Query Debugging:** The SQLite query drops the crucial telemetry records due to a subtle timezone/string-matching bug (the database uses UTC ISO8601 strings, but the query logic truncates or misaligns the query bounds).

**Your Objectives:**
1. Fix `/home/user/triage.sh` so that it correctly:
   - Uses `ffprobe` to extract `pkt_duration_time` for all video frames.
   - Computes the cumulative exact duration (preventing precision loss).
   - Finds the exact 0-based `frame_idx` where the cumulative time *strictly exceeds* `5.500000` seconds.
   - Queries `/home/user/telemetry.db` (table `events`) for the exact 3 rows where `frame_idx` is strictly greater than the critical frame index.
   - Saves these 3 rows as a well-formatted JSON array to `/home/user/incident_data.json`.
2. Fix and start `/home/user/server.sh` so that it runs a persistent HTTP server on `0.0.0.0:8080`.
   - The server must respond to `GET /api/incident` with HTTP 200 OK and the exact contents of `/home/user/incident_data.json`.
   - The server must also accept an `Authorization: Bearer triage-token-99` header (rejecting others with 401 Unauthorized).

Leave the fixed server running in the background.

*Note: You may install tools like `jq`, `sqlite3`, `socat`, or `python3` to assist with the server and JSON formatting, but the primary logic must be fixed in the bash scripts.*