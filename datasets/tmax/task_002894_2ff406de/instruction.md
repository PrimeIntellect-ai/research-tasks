You are a data scientist troubleshooting an ETL pipeline that handles international user feedback.

The ETL pipeline had an issue where it would hang and then automatically retry, leading to duplicated records in our raw data logs. A screen recording of the pipeline's telemetry dashboard was captured during a 60-second ingestion window, saved at `/app/telemetry.mp4`. 

Your task involves combining video analysis, text processing, and data serving:

1. **Anomaly Detection via Video:**
   The video `/app/telemetry.mp4` runs for exactly 60 seconds at 1 FPS. During normal operation, the dashboard displays a test pattern. When the pipeline crashed and retried, the dashboard went completely black. 
   Use `ffmpeg` (which is pre-installed) to detect the exact seconds where the video frames are completely black. These timestamps represent the "retry windows" (e.g., if seconds 12, 13, and 14 are black, the retry window is 12-14 seconds inclusive).

2. **Dataset Cleaning & Deduplication:**
   You are provided with a raw data file at `/home/user/feedback.jsonl`. Each line is a JSON object with `id`, `ingest_time_sec` (integer from 0 to 59, corresponding to the video second), `email`, and `feedback_text` (which contains multi-language Unicode text).
   Because of the pipeline retries, any record whose `ingest_time_sec` falls exactly within a "retry window" (the black frames) is highly suspect and might be duplicated. 
   *Rule:* If multiple records within the same retry window have the exact same `email`, keep only the **first** occurrence (lowest `id`) and drop the rest.

3. **Data Masking:**
   For all records that remain after deduplication, mask the `email` field by replacing the entire local part (everything before the `@` symbol) with `[MASKED]`. (e.g., `john.doe@example.com` becomes `[MASKED]@example.com`).

4. **Serve the Results:**
   Compute the following summary statistics:
   - `total_raw`: Total number of records in the original file.
   - `total_cleaned`: Total number of records remaining.
   - `removed_ids`: A JSON array of the `id`s of the duplicate records that were removed.
   
   Write a program (in Python or your language of choice) that listens on `127.0.0.1:8080` and serves:
   - `GET /stats`: Returns a JSON object with the summary statistics (`total_raw`, `total_cleaned`, `removed_ids`).
   - `GET /cleaned`: Returns the cleaned and masked JSONL data (Content-Type: text/plain).

Keep this service running in the background so it can be verified.