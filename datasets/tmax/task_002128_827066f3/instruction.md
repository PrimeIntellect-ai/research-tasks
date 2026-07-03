You are a data engineer tasked with building a tiny, Bash-only ETL pipeline to recover telemetry data embedded in a video file and serve it to downstream services.

An automated drone recorded a video and embedded its telemetry stream as a subtitle track (SRT format) inside the MP4 file located at `/app/telemetry.mp4`. However, the telemetry ingestion system had a bug, producing malformed JSON-lines, and the data is in the wrong shape for our analytics database.

Write a Bash script at `/home/user/pipeline.sh` that performs the following steps when executed:

1. **Stream Extraction:** Use `ffmpeg` to extract the subtitle track (stream `0:s:0`) from `/app/telemetry.mp4` to standard output or a temporary file.
2. **Streaming Cleaning:** Filter the SRT output to only keep the lines that start with `{` (the actual JSON payloads). 
3. **Anomaly Correction:** The JSON-lines parser breaks because the telemetry software incorrectly encoded spaces in its "status" field as `\u002X` instead of `\u0020`. Use a text-processing tool (like `sed`) to fix this unicode escape sequence anomaly.
4. **Reshaping (Wide to Long):** The corrected JSON lines have a wide format: `{"ts": <unix_timestamp>, "t": <temperature_celsius>, "h": <humidity>, "status": "..."}`. Use `jq` to reshape this into a long-format CSV with three columns: `timestamp,metric,value`. For each JSON record, generate two CSV lines (one for `t` and one for `h`).
5. **Imputation & Normalization:**
   - If `h` (humidity) is missing or null, impute it with a default value of `50.0`.
   - Standardize the `t` (temperature) metric by converting it from Celsius to Fahrenheit ($F = C \times 1.8 + 32$). You can use `awk` to perform this math on the CSV stream.
6. **Persistence & Serving:** 
   - Save the fully processed CSV data (without headers) to `/home/user/clean_telemetry.csv`.
   - Start a simple HTTP server listening on TCP port `8080` (using `nc` or `socat`). When it receives a request, it must respond with a valid `HTTP/1.1 200 OK` header, a blank line, and the contents of `/home/user/clean_telemetry.csv`. It only needs to serve one request and then can exit.

Ensure your script is executable (`chmod +x /home/user/pipeline.sh`) and runs the entire extraction, transformation, and serving process when invoked.