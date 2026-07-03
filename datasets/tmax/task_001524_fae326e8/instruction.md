You are a data engineer tasked with building an ETL pipeline that processes incoming audio and telemetry data, normalizes it, and serves the aggregated results via a simple HTTP microservice. You must use only Bash, standard shell utilities (awk, sed, grep, iconv, etc.), and `nc` or `socat` for the server.

You have the following inputs:
1. **Audio Artefact:** A transmission file located at `/app/audio/transmission.wav`.
2. **Telemetry Data:** A directory `/app/data/telemetry/` containing hundreds of CSV files (e.g., `sensor_001.csv`, `sensor_002.csv`). Each CSV has the format `timestamp,value` (e.g., `1700000000,42.5`). 

Your ETL workflow must perform the following:

**Step 1: Audio Extraction & Unicode Normalization**
The audio file contains embedded metadata. You can extract the raw transcript by searching the binary WAV file for a string starting with `TRANSCRIPT_DATA:` (using standard tools like `strings`). 
The extracted transcript contains mixed encodings and non-standard Unicode characters. You must normalize this text to standard ASCII (transliterating where possible, dropping where not) to prevent downstream encoding issues. 

**Step 2: Resampling & Gap-Filling Telemetry (Parallel Processing)**
The sensor logs are recorded irregularly. You must process all CSV files in `/app/data/telemetry/` in parallel (using tools like `xargs -P` or `find -exec`). 
For each file, resample the time-series data to exactly 1Hz (1 second intervals) from the minimum timestamp to the maximum timestamp found in that file. Use forward-fill (carry over the last known value) for any missing seconds. 
After resampling, calculate the global maximum value across all filled sensor data.

**Step 3: Serve via HTTP**
Build a lightweight bash-based HTTP server listening on `127.0.0.1:8080`.
When it receives an HTTP GET request to `/`, it must respond with a valid `HTTP/1.1 200 OK` header, followed by a JSON payload containing:
```json
{
  "transcript": "<YOUR_NORMALIZED_ASCII_TRANSCRIPT>",
  "global_max": <MAX_VALUE_FOUND>
}
```

The server must stay alive to serve multiple requests. Run it in the background or in a continuous loop. Write all your logic into a script at `/home/user/etl_server.sh` and execute it.