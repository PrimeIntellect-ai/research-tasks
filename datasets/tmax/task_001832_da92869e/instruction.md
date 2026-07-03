You are an on-call engineer at VisionFlow, a traffic analytics startup. You've just been paged at 3am: our primary traffic counting API is returning wildly incorrect numbers, and the nightly batch processing job failed to build and run on the new environment.

Your task is to fix the pipeline, process last night's traffic video, and bring the API back online so the upstream dashboards can recover.

The system consists of two parts:
1. A Python video processing engine (`/home/user/vision_engine/`) that analyzes a traffic camera feed and logs vehicle crossings into a SQLite database.
2. A Node.js API service (`/home/user/api_service/`) that reads the database and serves the statistics via HTTP.

Here is what you need to do:

1. **Build Failure Diagnosis:** The Python engine's setup script (`/home/user/vision_engine/build.sh`) is failing. Fix the script so it correctly installs the required dependencies in a virtual environment.
2. **Formula Implementation Correction:** The core mathematical logic for detecting line crossings in the Python engine (`/home/user/vision_engine/detector.py`) has a bug. It calculates the intersection of the vehicle's trajectory with a virtual counting line using a 2D line intersection formula, but it's currently producing statistical anomalies (negative counts and missing crossing events). Correct the math formula.
3. **Process the Video:** Run the fixed Python engine on the provided raw video feed located at `/app/traffic_cam_04.mp4`. This will populate the local SQLite database (`/home/user/data/traffic.db`).
4. **Query Result Debugging:** The Node.js API service (`/home/user/api_service/server.js`) has a bug in its SQL query. It is supposed to return the total count of northbound and southbound vehicles per hour, but it's currently grouping incorrectly and dropping records. Fix the SQL query.
5. **Start the API:** Start the Node.js service. It must listen on `0.0.0.0:8080`. It has a single endpoint: `GET /api/stats?auth=vision2024`.

Leave the API running in the background when you are done. The automated recovery checker will verify the system by sending HTTP requests to `http://localhost:8080/api/stats?auth=vision2024` and validating the JSON response against the ground truth counts from `/app/traffic_cam_04.mp4`.

Ensure all code changes are saved and the API service remains active.