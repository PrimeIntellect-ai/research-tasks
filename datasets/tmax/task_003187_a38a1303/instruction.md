You are a data engineer tasked with building an ETL pipeline to process time-series sensor data. 

We have a set of raw sensor readings in `/app/sensor_data.csv` (columns: `timestamp,sensor_id,value`). We also have a legacy system schematic in an image at `/app/legacy_metadata.png` which contains some critical configuration parameters that you must extract using OCR (e.g., `tesseract`).

Your objectives are:
1. Extract the `CRITICAL_ANOMALY_THRESHOLD` (an integer) and `TARGET_SENSOR` (a string) from the text within `/app/legacy_metadata.png`.
2. Write a C++ data processing pipeline (use C++17 or later) that reads `/app/sensor_data.csv` and calculates the following for each sensor concurrently (using parallel processing):
   - `min`, `max`, and `mean` of the values.
   - The number of anomalies, defined as any value that is strictly greater than `mean + 3 * stddev` or strictly less than `mean - 3 * stddev` (calculated per sensor).
   - A boolean `flagged` status, which is `true` if the number of anomalies exceeds the `CRITICAL_ANOMALY_THRESHOLD` extracted from the image, and `false` otherwise.
3. Compute the Euclidean distance between the time series of the `TARGET_SENSOR` and all other sensors (assuming all sensors have readings at the exact same timestamps, ordered chronologically) to find the single most similar sensor (minimum Euclidean distance).
4. Launch an HTTP server listening on `127.0.0.1:9090`. You may implement the server in C++ (using a library or raw sockets) or write a Python wrapper that serves the data processed by your C++ program. 
   The server must handle the following endpoints:
   - `GET /stats?sensor_id=<id>`: Return a JSON response like `{"min": 1.2, "max": 9.8, "mean": 5.5, "anomalies": 2, "flagged": false}`. Provide values rounded to 2 decimal places.
   - `GET /similar`: Return a JSON response identifying the most similar sensor to the target sensor: `{"target": "S42", "most_similar": "S15", "distance": 12.34}` (distance rounded to 2 decimal places).

Ensure the server stays running in the foreground or as a background process so it can be queried by our automated verification suite.