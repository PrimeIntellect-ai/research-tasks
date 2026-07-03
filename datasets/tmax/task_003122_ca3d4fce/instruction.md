You are a data analyst for a smart-city traffic monitoring system. You have been tasked with analyzing telemetry from traffic cameras, but the system has recently been targeted by malicious actors injecting bad data to crash our analytics pipelines. 

You must build a robust data pipeline that extracts real telemetry, validates it against malicious inputs, and computes optimized analytical queries.

**Step 1: Video Telemetry Extraction**
We have recovered a raw video file from a compromised edge node at `/app/sensor_feed.mp4`. 
Use `ffprobe` to extract the packet presentation time (`pkt_pts_time`) and packet size (`pkt_size`) for every video frame in this file. Save this data as a headless CSV to `/home/user/extracted_frames.csv`. 

**Step 2: Schema Validation & Sanitisation**
You must write a Python script `/home/user/validate_schema.py` that takes a single file path as a CLI argument. 
This script must validate the CSV file according to our strict telemetry schema:
1. Column 1: `timestamp` (must be a valid, non-negative floating-point number).
2. Column 2: `size` (must be a valid integer strictly greater than 0).
3. The file must not contain any hidden SQL injection payloads, executable strings, or malformed delimiters. 

If the entire file is clean and strictly adheres to the schema, the script MUST exit with code `0`. 
If ANY row in the file violates the schema or contains anomalous strings, the script MUST exit with code `1`.

**Step 3: Database Ingestion & Optimization**
A directory of historical telemetry files is located at `/app/historical_data/`. Some of these files are clean, and some are malicious.
1. Run your `validate_schema.py` script against all CSVs in `/app/historical_data/` and your newly generated `/home/user/extracted_frames.csv`.
2. Load ONLY the clean files into a SQLite database at `/home/user/telemetry.db` in a table named `frames` (`timestamp REAL, size INTEGER`).
3. Design and create an index strategy on the `frames` table that optimizes a time-based window query.
4. Write and execute an optimized SQL query (using Window Functions / CTEs) that calculates the largest frame `size` for each 1-second tumbling window (e.g., [0.0, 1.0), [1.0, 2.0)). 
5. Export the results to `/home/user/max_frames_per_sec.csv` with the headers `window_start, max_size`.

Ensure your database indexes are optimized so the query avoids full table sorts where possible.