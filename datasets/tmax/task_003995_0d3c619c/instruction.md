You are assisting a researcher in organizing a multi-modal dataset containing video, sensor logs, and hierarchical category annotations. 

Your objective is to extract insights using shell utilities, `ffmpeg`, `sqlite3`, and `jq`, and then expose the results via a simple HTTP server.

**Step 1: Video Analysis**
There is a video file located at `/app/experiment.mp4`. Use `ffmpeg` or `ffprobe` to determine the exact total number of frames in the video video streams.

**Step 2: Sensor Data Aggregation (Window Functions)**
A SQLite database at `/app/sensors.db` contains a table `readings` with columns `id` (INTEGER), `timestamp` (INTEGER), and `value` (REAL). 
Write a query to compute the 3-row moving average (the current row and the two preceding rows based on `timestamp` order) for the `value` column. Find the `id` of the row that has the highest moving average.

**Step 3: Taxonomy Processing (Recursive/Hierarchical Extraction)**
A JSON file at `/app/taxonomy.json` contains a nested tree structure representing experiment classifications. Each node has a `name` and an optional `children` array. Use `jq` to traverse this hierarchy and find the dot-separated path (e.g., `root.subcat1.TargetAnomaly`) to the node with the name `"TargetAnomaly"`.

**Step 4: Data Integration & Serving**
Combine the results from the first three steps into a single JSON file named `data.json` with the following exact structure:
```json
{
  "total_frames": <integer>,
  "max_sensor_id": <integer>,
  "anomaly_path": "<string>"
}
```
Place `data.json` in a new directory `/home/user/www`.
Finally, start an HTTP server on port `8080` serving the contents of `/home/user/www`. Ensure the server binds to `0.0.0.0:8080` and runs continuously in the background (or foreground if you prefer, but it must be running when your task finishes) so that a `GET /data.json` request returns your JSON payload. You may use standard CLI tools (like `python3 -m http.server`, `busybox httpd`, or `nc`) to serve the file.