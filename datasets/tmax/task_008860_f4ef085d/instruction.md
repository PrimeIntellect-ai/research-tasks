You are a data scientist tasked with building a data cleaning pipeline for a set of vehicle sensor logs. 

We have a corrupted sensor log file located at `/home/user/data/sensor_logs.csv`. The file is encoded in `Windows-1252` and contains telemetry data from a delivery truck. The dataset is too large to comfortably fit into memory on our production micro-containers, so you must process it efficiently (e.g., using streaming, generators, or chunking).

The CSV has the following columns:
`timestamp,lat,lon,temperature`

Your objective is to write and execute a Python script that performs the following steps:

1. **Character Encoding & Streaming:** Read the input CSV file line-by-line or in chunks, handling the `Windows-1252` encoding.
2. **Anomaly Detection (Distance Computation):** Calculate the Haversine distance between consecutive geographical points (lat/lon). Due to GPS glitches, some points jump impossibly far. 
   - If the implied speed between the *last valid point* and the *current point* exceeds **250 meters per second**, the current point is an anomaly and must be **dropped**. 
   - The first row of data is always considered valid.
   - Use an Earth radius of exactly `6371.0` km for Haversine calculations.
3. **Imputation:** The `temperature` sensor periodically drops out, leaving empty values in the CSV. Impute these missing temperature values using **linear interpolation** based on the `timestamp` (which are integer Unix epoch seconds). 
   - The first and last temperature values in the dataset are guaranteed to be present.
   - Interpolation should only occur *after* anomalous GPS points are dropped.
4. **Data Output:** Save the cleaned, interpolated dataset to `/home/user/processed_logs.jsonl`. This must be a UTF-8 encoded JSON Lines file, where each line is a JSON object with keys: `"timestamp"` (int), `"lat"` (float), `"lon"` (float), and `"temperature"` (float rounded to 2 decimal places).
5. **Local Serving:** Create a directory `/home/user/server_root`. Inside it, create a file named `summary.json` containing the exact JSON structure:
   `{"total_valid_distance_km": <float>, "final_row_count": <int>}`
   - `total_valid_distance_km` is the cumulative Haversine distance of the cleaned trajectory, rounded to 2 decimal places.
   - Start a standard Python HTTP server serving this directory on port `8080` in the background (e.g., `python3 -m http.server 8080 -d /home/user/server_root &`).

Ensure all scripts are run and the background server is active before you finish.