You are an automation specialist tasked with building a video telemetry extraction pipeline. We have a dashboard recording video (`/app/dashboard_recording.mp4`) and a raw telemetry dump in JSON-Lines format (`/app/telemetry_stream.jsonl`). 

Your objective is to process these two data sources, correlate them, and serve the results via an HTTP REST API.

Here are the requirements:

1. **Telemetry Normalization**: 
   The file `/app/telemetry_stream.jsonl` contains one JSON object per line. However, the system that generated it produced malformed unicode escape sequences (e.g., `\uXXXX` where it shouldn't, or truncated sequences). You must write a Python script using regex and string manipulation to clean and parse this file. Each valid telemetry record contains a `"frame_index"` (integer) and a `"sensor_reading"` (string). Drop any lines that cannot be recovered or parsed into valid JSON after normalization.

2. **Video Feature Extraction**:
   Use `ffmpeg` (which is preinstalled) and Python to process `/app/dashboard_recording.mp4`. Extract the frames and calculate the average grayscale brightness (pixel intensity from 0 to 255) for each frame. Identify all "flash events" — defined as frames where the average brightness is strictly greater than 200.0.

3. **Data Correlation**:
   Match the "flash events" from the video with the cleaned telemetry data. For every frame index that is identified as a flash event, find the corresponding `"sensor_reading"` from the parsed JSON-lines data. 

4. **Service Endpoint**:
   Create a Python HTTP server (e.g., using Flask, FastAPI, or `http.server`) listening on `127.0.0.1:8080`.
   - Endpoint: `GET /api/v1/flash-telemetry`
   - Authentication: The server must require a Bearer token in the Authorization header. The required token is `SecretAdminToken99`. If the token is missing or incorrect, return a 401 Unauthorized status.
   - Response: On a successful, authenticated request, return a 200 OK status with a JSON payload in this exact format:
     ```json
     {
       "flash_events": [
         {
           "frame_index": 12,
           "brightness": 215.4,
           "sensor_reading": "temperature_critical"
         },
         ...
       ]
     }
     ```
     (Sort the events in ascending order by `frame_index`).

You must run this server in the background so that our automated test suite can verify your implementation by sending HTTP requests to `http://127.0.0.1:8080/api/v1/flash-telemetry`. Let me know when the server is up and running.