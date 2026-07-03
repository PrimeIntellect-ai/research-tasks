You are an automation specialist building a sensor data processing workflow. We have a multi-service setup consisting of an Nginx web server, a Redis instance, and a custom Go worker you need to write.

Currently, raw sensor data files (in either CSV or JSON format) are uploaded to a web server. We need a Go-based worker process that continuously polls a Redis queue for new file names, downloads the files via HTTP, processes the time-series data to detect anomalies, and writes the classification results back to Redis.

Here are the requirements for your Go worker:
1. **Queue Processing**: Connect to Redis at `localhost:6379`. Continuously read from the Redis list `processing_tasks` (using a blocking pop operation like `BLPOP`). The value popped will be a filename (e.g., `sensor_123.csv` or `sensor_456.json`).
2. **File Fetching**: Download the file from the local Nginx server at `http://localhost:8080/data/<filename>`.
3. **Data Parsing**: 
   - If the file ends in `.csv`, parse it as a CSV with columns `timestamp,temperature`.
   - If the file ends in `.json`, parse it as a JSON array of objects: `[{"timestamp": "...", "temperature": 20.5}, ...]`.
   - The `temperature` field might be missing, null (in JSON), or an empty string (in CSV).
4. **Imputation**: For any missing `temperature` values, perform linear interpolation using the nearest preceding and succeeding valid temperature values. (You can assume the first and last values in every file are never missing).
5. **Rolling Statistics & Anomaly Detection**:
   - Compute a 3-point rolling average for the temperature (the average of the current point and the two immediately preceding points). For the first two points, just average the available points.
   - A file is classified as `EVIL` (anomalous) if *any* point's interpolated temperature strictly exceeds the 3-point rolling average by more than `15.0` degrees.
   - Otherwise, the file is classified as `CLEAN`.
6. **Result Output**: For each processed file, push a string in the format `<filename>:<RESULT>` (e.g., `sensor_123.csv:CLEAN` or `sensor_456.json:EVIL`) to the Redis list `processing_results` using `RPUSH`.

**Environment details**:
- Nginx and Redis are already installed. You must start them. Nginx is configured to serve files from `/app/data` on port 8080.
- You must write your worker in Go at `/home/user/worker.go` and compile/run it.
- Your worker should handle the end-to-end flow so that when a test script pushes a batch of filenames to Redis, the classifications appear in `processing_results`.

Start the services, implement the Go worker, and leave it running in the background so the automated verification system can test it against a hidden corpus of clean and evil files.