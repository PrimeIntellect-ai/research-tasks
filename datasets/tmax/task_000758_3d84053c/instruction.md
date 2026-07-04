You are a data analyst dealing with a legacy telemetry system. We have a daily export of telemetry logs in a CSV file, but the payload column is obfuscated and mixed with weird character encodings.

Your objective is to build a data processing pipeline in Python that extracts, decodes, aggregates this data, and serves the results via a live HTTP REST API.

Here are the requirements:
1. **Data Source**: The input file is located at `/home/user/data/telemetry.csv`. It has three columns: `timestamp` (ISO 8601 format), `source_ip`, and `raw_payload`.
2. **Encoding Handling**: The `raw_payload` strings were corrupted during export. They contain a mix of UTF-8, UTF-16LE, and Windows-1252 encoded byte sequences represented as hex strings (e.g., `54686973...`). You must safely decode these hex strings to raw bytes, ignoring uninterpretable characters, and convert them to standard UTF-8 strings.
3. **Obfuscation Reversal**: We have a legacy, stripped binary located at `/app/log_decoder`. You must pass the cleaned UTF-8 string to this binary as a command-line argument. The binary will output a structured key-value string (e.g., `STATUS=OK|CPU_TEMP=45.2|MEM_USAGE=80`).
4. **Parallel Processing**: Because the CSV is large and calling the binary is slow, you must implement parallel processing (e.g., using Python's `concurrent.futures` or `multiprocessing`) to process the rows efficiently.
5. **Time-Based Aggregation**: Extract the `CPU_TEMP` float value from the binary's output for each row. Aggregate these values into 1-hour time buckets (e.g., `2023-10-24T14:00:00Z` to `2023-10-24T14:59:59Z`). Calculate the average `CPU_TEMP` for each hour bucket. Ignore rows where `CPU_TEMP` is missing or invalid.
6. **Live Service**: Create and run a Python HTTP server (e.g., using Flask, FastAPI, or `http.server`) listening on `127.0.0.1:8080`.
    * It must have an endpoint `GET /api/temperature?hour=YYYY-MM-DDTHH:00:00Z`
    * The endpoint must return a JSON response in this exact format: `{"hour": "YYYY-MM-DDTHH:00:00Z", "avg_cpu_temp": 45.25}` (rounded to 2 decimal places).
    * If the hour bucket does not exist, return a 404 status code with `{"error": "Not found"}`.

Start the server as a background process or leave it running in the foreground (our testing framework will ping it). Do not use external databases; keep the aggregated data in memory.