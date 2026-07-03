You are a data analyst investigating a series of anomalies in a logistics network. You have been given a network graph of vehicle movements scattered across undocumented CSV files, and a video feed from a traffic sensor. 

Your task involves processing this data, matching specific patterns in the graph, and exposing your findings via an HTTP API.

1. **Video Analysis (`/app/traffic_sensor.mp4`)**:
   The video contains 60 seconds of traffic sensor data at 10 frames per second. Most frames are dark (black). However, sensor "pings" appear as entirely white frames. Use `ffmpeg` and Python to extract the exact frame numbers of all white frames (where average pixel brightness is > 200). These frame numbers correspond directly to `ping_id`s in the network data.

2. **Data Model Reverse Engineering (`/home/user/logistics_data/`)**:
   This directory contains several undocumented CSV files with randomized names. You must reverse-engineer the schema to identify:
   - The "Nodes" file (contains entities: drivers, vehicles, pings).
   - The "Edges" file (contains relationships: `drove`, `detected_at`).
   
3. **Knowledge Graph Pattern Matching**:
   Construct a knowledge graph from the CSV files. You need to find all "Driver" nodes that are connected (via a "Vehicle") to the specific `ping_id`s you extracted from the video. 
   
4. **API Service**:
   You must build and start a Python HTTP service (e.g., using Flask or FastAPI) listening on `127.0.0.1:8080`.
   - **Endpoint**: `POST /api/investigate`
   - **Request**: Accepts a JSON payload `{"video_ping_ids": [list of integers]}`.
   - **Response**: Must return a JSON object containing the matched drivers, strictly validating against this schema:
     ```json
     {
       "type": "object",
       "properties": {
         "suspect_drivers": {
           "type": "array",
           "items": { "type": "string" }
         }
       },
       "required": ["suspect_drivers"]
     }
     ```
     The array must be sorted alphabetically.

The service must remain running in the foreground or background so the verification system can query it. Make sure to install any required Python packages (e.g., `flask`, `networkx`, `opencv-python-headless`) using pip.