You are a data analyst and backend developer. You have been provided with a directory of undocumented CSV files extracted from a legacy traffic monitoring system, along with a synchronized video recording of the intersection.

Your task is to reverse engineer the data model, load the data to query it efficiently, and build a Rust-based HTTP API that serves specific frames from the video based on aggregated cross-query results.

**Resources:**
1. **Video File:** `/app/footage.mp4` (a traffic camera recording, 30fps).
2. **CSV Files:** Located in `/home/user/data/`. There are three files: `table_alpha.csv`, `table_beta.csv`, and `table_gamma.csv`. You must analyze their headers and data to understand their foreign-key relationships. They represent 'events', 'object_classifications', and 'sensor_confidence_scores'.

**Requirements:**
1. **Data Model Reverse Engineering:** Analyze the CSVs. One table contains the event timestamp (in seconds), another contains the object category string, and the third contains confidence scores for various detections. 
2. **Rust Web Service:** Create a Rust HTTP server in `/home/user/traffic-api` (initialize a new cargo project). You may use standard libraries or lightweight crates like `rouille` or `tiny-http`.
3. **API Endpoint:** The server must listen exactly on `127.0.0.1:5050`.
4. **Route:** `GET /highest-confidence-frame?category={category_name}`
5. **Logic:**
   - For the given string `{category_name}` (e.g., "truck", "bicycle"), perform a cross-query aggregation across the three CSV datasets to find the single event with the highest combined confidence score for that specific category.
   - Retrieve the `timestamp_sec` for that exact event.
   - Use `ffmpeg` (which is pre-installed) to extract the exact video frame at that timestamp from `/app/footage.mp4`.
   - Serve the extracted frame as a JPEG image (Content-Type: image/jpeg) in the HTTP response body.
   - Include a custom HTTP header `X-Event-Timestamp` containing the exact timestamp value used.
6. **Security:** The endpoint MUST require an `Authorization` header with the exact value `Bearer super-analyst-2024`. Requests without this or with an incorrect token must return a 401 Unauthorized status.
7. **Performance:** Ensure your Rust application executes the data queries efficiently (e.g., using parameterized queries against an in-memory SQLite database loaded via a bash initialization script, or directly using Rust).

Start the server in the background and leave it running. Do not exit the terminal until the server is successfully bound and listening on `127.0.0.1:5050`.