You are a data engineer building a real-time ETL pipeline for a smart city dashboard. We have an incoming traffic camera feed that needs to be processed, transformed, and served via a REST API.

Your task has three main phases:

**Phase 1: Feature Extraction & Timestamp Alignment**
A video artifact is located at `/app/traffic_feed.mp4`.
1. Analyze the video using Python (e.g., `cv2` or `ffmpeg`). Assume the video was recorded at exactly 25 FPS (40ms per frame).
2. The very first frame (index 0) corresponds to the timestamp `2024-05-01T08:00:00.000Z`.
3. For each frame, extract the "brightness" feature: convert the frame to grayscale and calculate the mean pixel intensity (float).
4. Align each frame with its exact timestamp based on the 25 FPS frame rate.

**Phase 2: Rolling Statistics & Reshaping**
1. Compute a rolling average of the brightness over a window of 5 frames (the current frame and the 4 preceding frames). 
2. For the first 4 frames where a full window is not available, calculate the mean of whatever frames are available so far (e.g., the 2nd frame's rolling average is just the mean of frame 0 and frame 1).
3. Reshape the data from a "wide" format to a "long" format. The target format should have records with three fields: `timestamp` (ISO8601 string, Z-suffixed), `metric` (either `"brightness"` or `"rolling_avg"`), and `value` (float, rounded to 2 decimal places).

**Phase 3: HTTP Serving**
Build and start a Python web server (e.g., using Flask or FastAPI) that serves this transformed data.
- **Listen Address:** `127.0.0.1:8080`
- **Endpoint:** `GET /api/v1/telemetry`
- **Authentication:** Must require an `Authorization` header with the exact value `Bearer TRL-992-DATA`. Return a 401 Unauthorized HTTP status otherwise.
- **Query Parameters:** `start` and `end` (both ISO8601 strings). Return all data points where the timestamp is `>= start` and `<= end`.
- **Response Format:** A JSON array of objects in the long format described above, sorted chronologically by timestamp, then alphabetically by metric name.

Example response structure:
```json
[
  {"timestamp": "2024-05-01T08:00:00.000Z", "metric": "brightness", "value": 112.45},
  {"timestamp": "2024-05-01T08:00:00.000Z", "metric": "rolling_avg", "value": 112.45},
  {"timestamp": "2024-05-01T08:00:00.040Z", "metric": "brightness", "value": 115.10}
]
```

Keep the server running in the foreground or background so our automated verifier can query it.