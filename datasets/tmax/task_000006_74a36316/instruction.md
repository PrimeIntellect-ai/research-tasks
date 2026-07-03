**PagerDuty Alert: CRITICAL**
**Time:** 03:14 AM
**Service:** VisionMath-Analytics
**Issue:** The real-time video analytics service is returning `NaN` in its JSON payload, dropping TCP connections, and randomly crashing under load. Downstream clients are failing to parse the coordinates.

You are the on-call engineer. The broken service is located in `/home/user/vision_math/`.

**System Overview:**
The VisionMath service reads a continuous video feed, computes the centroid (brightest pixel) of the moving object, and calculates the running standard deviation of the object's X and Y coordinates. 

It exposes two endpoints:
1. **HTTP JSON API (Port 8080):** A GET request to `/latest` should return `{"x": <double>, "y": <double>, "stddev_x": <double>, "stddev_y": <double>}`.
2. **Binary TCP Stream (Port 8081):** Upon connection, the server should immediately send exactly 32 bytes representing 4 `double`s (little-endian: x, y, stddev_x, stddev_y) of the latest state, then close the connection.

**Symptoms to Debug & Fix:**
1. **Precision/Math Bug:** The standard deviation frequently becomes `NaN` due to catastrophic cancellation in the naive variance formula currently implemented in `server.cpp`. You must replace it with a numerically stable algorithm (e.g., Welford's method).
2. **Race Conditions:** The video processing thread and the network serving threads access the shared state without proper synchronization, causing garbage data over TCP and random segmentation faults. 
3. **Serialization:** The JSON encoder fails or produces invalid JSON when memory corruption occurs.

**Your Tasks:**
1. Inspect and debug `/home/user/vision_math/server.cpp`.
2. Fix the mathematical precision loss, race conditions, and serialization bugs.
3. The service processes a test video located at `/app/trajectory_test.mp4`. The code already contains the logic to shell out to `ffmpeg` to extract frames—ensure it reads the correct file.
4. Compile the fixed service: `g++ -O2 -std=c++17 -pthread server.cpp -o server`.
5. Run the service in the background so it listens on `127.0.0.1:8080` (HTTP) and `127.0.0.1:8081` (TCP).
6. Leave the process running. The automated verification system will issue concurrent HTTP and TCP requests to validate the correctness of the mathematical output and the stability of the server.