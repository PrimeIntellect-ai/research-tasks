You are an automation specialist responsible for creating a real-time telemetry processing pipeline. 

We have a proprietary, stripped binary located at `/app/stream_gen`. This binary generates a continuous, large stream of system events. However, it requires a specific hidden activation flag to start outputting data. You will need to inspect the binary to find this flag.

When executed with the correct flag, the binary outputs lines to `stdout` in the following pipe-separated format:
`[Unix Timestamp]|[Multilingual Status Tag]|[Numeric Value]`
*(Example tags include Unicode strings like "正常", "エラー", "警告", "успех", "ошибка".)*

Your task is to build a multi-language workflow that does the following:

1. **Stream Processing & Aggregation Pipeline:**
   Write a script (e.g., in Python or Node.js) that reads the continuous output of `/app/stream_gen` via `stdin`.
   As the data streams in, maintain a **rolling 60-second window** of the data. 
   Continuously calculate the average of the `[Numeric Value]` for each distinct `[Multilingual Status Tag]` within the last 60 seconds (based on the timestamps in the stream, not system time).

2. **Real-time API Service:**
   Expose these rolling aggregations via a local HTTP web service. 
   - **Host/Port:** The service must listen exactly on `127.0.0.1:8080`.
   - **Endpoint:** `GET /metrics`
   - **Authentication:** The endpoint must require an `Authorization: Bearer DataFlow2024` header. If missing or incorrect, return a `401 Unauthorized` status.
   - **Response Format:** Return a JSON object where keys are the Unicode status tags and values are the computed averages (as floats) for the trailing 60-second window. Example: `{"エラー": 45.2, "正常": 12.0}`

3. **Pipeline Scheduling (Cron):**
   Set up a cron job for the current user that runs every minute. 
   The cron job must query the `GET /metrics` endpoint (passing the correct auth token) and append the raw JSON response as a new line to `/home/user/rolling_archive.jsonl`.

*Constraints & Notes:*
- Ensure your pipeline handles large, continuous streams without loading unbounded amounts of data into memory (drop old data from the window).
- Properly handle UTF-8 encoding for the multilingual tags.
- Use Bash for plumbing and cron, and your choice of language (e.g., Python) for the data processing and API server.
- Leave the API server running in the background so it can be verified.