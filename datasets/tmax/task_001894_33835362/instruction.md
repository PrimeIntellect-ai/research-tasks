You are tasked with building a Configuration Drift Tracker for our DevOps team. Our team recently photographed a whiteboard detailing the canonical baseline server configuration for our data center. This image has been uploaded to `/app/config_baseline.png`.

Your task is to create a Go-based HTTP service that extracts this baseline configuration, accepts incoming configuration reports from running servers, validates them, and computes a "drift score" to quantify how far the running server has deviated from the baseline.

Here are the requirements for the system:

1. **Baseline Feature Extraction:**
   - Use Tesseract OCR (which is preinstalled) to extract the text from the image located at `/app/config_baseline.png`.
   - The image contains four key pieces of information in a key-value format (Hostname, Cores, Memory, Storage). You must parse this text in your Go application to establish the baseline state. Assume memory is always an integer representing GB.

2. **HTTP Service Setup:**
   - Write a Go application (in `/home/user/drift_tracker.go`) and compile/run it.
   - The server must listen on `127.0.0.1:8080`.
   - The server must implement a single endpoint: `POST /api/v1/drift`.
   - The endpoint must require authentication. It must reject requests that do not have the header `Authorization: Bearer devops-secret-token` with an HTTP 401 status code.

3. **Incoming Data Validation:**
   - The `POST /api/v1/drift` endpoint will receive a JSON body representing a server's current state:
     ```json
     {
       "hostname": "string",
       "cores": int,
       "memory_gb": int,
       "storage": "string"
     }
     ```
   - Before calculating drift, validate the payload. If `cores` is <= 0 or `memory_gb` is <= 0, the server must return an HTTP 400 Bad Request with the JSON response `{"status": "invalid"}`.

4. **Drift Score Computation:**
   If the payload is valid, compute the Total Drift Score using the following metrics compared to the baseline extracted from the image:
   - **Hostname Drift:** The Levenshtein distance between the baseline hostname and the submitted hostname.
   - **Resource Drift:** The absolute difference between baseline cores and submitted cores PLUS the absolute difference between baseline memory and submitted memory.
   - **Storage Drift:** 0 if the storage strings match exactly (case-insensitive), otherwise 50.
   - **Total Drift** = Hostname Drift + Resource Drift + Storage Drift.

5. **Response Format:**
   - Return an HTTP 200 OK with the following JSON structure:
     ```json
     {
       "status": "valid",
       "total_drift": <integer>
     }
     ```

Make sure your Go server remains running in the background or foreground so it can be tested. You may use any standard Go libraries, and you can install third-party libraries (e.g., for Levenshtein distance) using `go get`. Do not hardcode the baseline values; your program must read and parse the Tesseract output.