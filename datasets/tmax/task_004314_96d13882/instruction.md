You are a log analyst investigating a messy data drop from a failed ETL pipeline. The pipeline experienced several retry loops, causing duplicate records in the raw log file. Furthermore, the configuration details for processing this log were lost in a system crash, but we managed to recover a screenshot of the configuration dashboard.

Your objective is to build a data processing pipeline that cleans the logs, extracts time-series features, and serves the results via a local HTTP API.

Here are the steps you must follow:

1. **Extract Configuration:**
   Inspect the image located at `/app/config_screenshot.png`. This image contains text outlining the system configuration. Use an OCR tool (like `tesseract`, which is installed) to extract two key parameters from this image:
   - `TARGET_PORT`: The port your API must listen on.
   - `RESAMPLE_INTERVAL`: The time frequency you must use for resampling the logs (e.g., "5min", "1H").

2. **Process the Logs:**
   The raw logs are located at `/app/logs/etl_dump.csv`. The file has three columns: `timestamp`, `user_id`, and `latency`.
   - **Deduplication:** The ETL job retried multiple times, causing exact duplicate rows. Remove all exact duplicates.
   - **Gap-filling & Resampling:** For each `user_id`, the time-series data has irregular gaps. You must resample the timeline for each user using the `RESAMPLE_INTERVAL` extracted from the image. 
   - When resampling, aggregate the `latency` using the **maximum** value in that interval.
   - If an interval has no data (a gap), forward-fill (`ffill`) the latency from the previous interval. If it's the very first interval and it's missing, leave it null/None.
   - *Hint: Consider using pandas and multiprocessing to handle the groupings efficiently if the dataset gets large.*

3. **Serve the Data:**
   Create and start a Python HTTP web server (e.g., using Flask or FastAPI) listening on `127.0.0.1` at the `TARGET_PORT` extracted from the image.
   
   The server must implement the following endpoint:
   - `GET /api/user_latency?user_id=<user_id>`
   
   The response must be a JSON array of objects, sorted chronologically by timestamp, in the following exact format:
   ```json
   [
     {
       "timestamp": "YYYY-MM-DD HH:MM:SS",
       "max_latency": 150.5
     },
     ...
   ]
   ```
   (Note: Omit entries where `max_latency` is null/NaN after forward-filling).

Leave the server running in the background so it can be verified.