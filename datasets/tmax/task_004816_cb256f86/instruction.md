You are a data engineer tasked with building an end-to-end ETL pipeline and serving layer for raw IoT sensor time-series data. 

We have received a messy dataset of sensor readings at `/home/user/raw_sensors.csv`. The file has columns: `timestamp`, `sensor_id`, and `value`. It contains duplicates, out-of-order rows, and missing values.

Additionally, your team lead left a screenshot of the target configuration dashboard at `/app/config.png`. You must extract the required time-bucketing interval and the API authentication token from this image. (You may use OCR tools like `tesseract`, which is installed on the system, to read the image).

Your task has two parts:

**Part 1: The ETL Pipeline**
Write a Python script that processes `/home/user/raw_sensors.csv` to:
1. Parse the timestamps and sort the data chronologically.
2. Deduplicate the records (if multiple rows have the exact same `timestamp` and `sensor_id`, keep the first one).
3. For each `sensor_id`, perform linear interpolation to fill in any missing (null/empty) `value`s.
4. Bucket the data into fixed time intervals. The exact interval size is written in the `/app/config.png` image (look for "INTERVAL"). Aggregate the `value`s in each bucket by calculating the mean.
5. Bulk load the processed data into a local SQLite database at `/home/user/processed.db` in a table named `sensor_data` with columns `time_bucket` (TEXT, format 'YYYY-MM-DD HH:MM:SS'), `sensor_id` (TEXT), and `avg_value` (REAL).

**Part 2: The Serving API**
Write and start a Python HTTP web server (e.g., using Flask, FastAPI, or standard library) that serves the processed data from the SQLite database.
1. The server must listen exactly on `127.0.0.1:8055`.
2. Expose a single HTTP GET endpoint: `/query?sensor_id=<sensor_id>`
3. The endpoint must enforce authentication. It should check for the `Authorization: Bearer <TOKEN>` header. The exact `<TOKEN>` value is also written in the `/app/config.png` image. If the token is missing or incorrect, return a 401 Unauthorized status.
4. If successful, the endpoint must query the SQLite database and return a JSON response containing an array of objects for the requested sensor, sorted by time. Format:
   `[{"time": "YYYY-MM-DD HH:MM:SS", "value": 25.4}, {"time": "...", "value": ...}]`

Start your server in the background and leave it running so our automated test suite can query it.