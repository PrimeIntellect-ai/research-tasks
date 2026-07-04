You are acting as a data analyst for a security firm. We have a video feed from a static security camera and a corresponding CSV log of sensor data. You need to build a pipeline to analyze the video, correlate it with the CSV, and serve your findings via a REST API.

Here are the details of your objective:

1. **Environment Setup**:
   - The video file is located at `/app/security_feed.mp4`.
   - The sensor data is at `/home/user/sensor_logs.csv`.
   - You may use standard Python libraries, `numpy`, `pandas`, `flask` (or `fastapi`), and `ffmpeg-python` or `subprocess` to call `ffmpeg`.

2. **Video Processing & Linear Algebra**:
   - Extract frames from `/app/security_feed.mp4` at 1 frame per second.
   - For each frame, convert it to grayscale. Treat the grayscale image as a matrix. Calculate the singular value decomposition (SVD) of each frame matrix. 
   - Compute the "complexity score" of each frame, defined as the sum of its top 10 singular values.

3. **Sampling & Bootstrap**:
   - Using the calculated complexity scores, use the bootstrap method (resampling with replacement, 1000 iterations) to estimate the 95% confidence interval for the *mean* complexity score.
   - Any frame whose complexity score is above the upper bound of this 95% confidence interval is flagged as an "anomaly".

4. **Benchmarking & Validation**:
   - Measure the average time taken to process a single frame (from extraction to SVD computation).
   - Read `/home/user/sensor_logs.csv`. It has columns `timestamp_sec` and `sensor_active` (0 or 1). 
   - Validate your anomalies by calculating the precision: the proportion of your flagged "anomaly" frames (where the frame index corresponds to `timestamp_sec`) that have `sensor_active == 1` in the CSV.

5. **API Serving (Multi-Protocol)**:
   - Create and run an HTTP API listening on `127.0.0.1:8080`.
   - The API must have the following endpoints:
     - `GET /stats`: Returns a JSON object with keys `lower_bound`, `upper_bound` (from the bootstrap CI), and `mean_inference_sec` (the average processing time per frame).
     - `GET /anomalies`: Returns a JSON object with the key `anomalous_frames` containing a list of integers (the frame indices/seconds flagged as anomalies).
     - `GET /validation`: Returns a JSON object with the key `precision` representing the calculated precision score.

Ensure the server is running continuously in the background so it can be queried by our automated verification suite.