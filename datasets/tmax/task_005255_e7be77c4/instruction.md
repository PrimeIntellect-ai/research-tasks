You are a data scientist cleaning up an interrupted ETL pipeline for IoT sensor time-series data. Due to an aggressive retry mechanism in the faulty ETL job, the resulting dataset has misaligned timestamps, duplicates, and missing periods. Additionally, a field technician left a voice memo detailing manual calibrations that must override the automated sensor readings.

Your objective is to build a robust C-based pipeline to process the raw data, apply the technician's corrections, and serve the cleaned data via a lightweight TCP server.

**Input Files:**
1. `/app/sensor_raw.csv`: A CSV file with headers `timestamp_ms,value`. Timestamps are in milliseconds.
2. `/app/corrections.wav`: An audio file containing the technician's spoken corrections in English. (You may use available shell tools like `whisper`, `ffmpeg`, or Python libraries to transcribe this, but the core processing and serving must be done in C).

**Data Processing Rules:**
1. **Timestamp Alignment:** Convert all `timestamp_ms` to nearest whole second (`timestamp_s = round(timestamp_ms / 1000.0)`).
2. **Deduplication:** The ETL retry bug created multiple entries for the same aligned second. Resolve collisions by keeping only the **maximum** `value` for that specific aligned second.
3. **Gap-Filling:** The data contains gaps. Apply **forward-filling** (carry over the last seen valid value) for any missing seconds between the minimum and maximum aligned seconds in the dataset.
4. **Validation/Overrides:** Parse the transcript of `/app/corrections.wav`. It will dictate specific timestamps and their true values (e.g., "timestamp 1680000005 has value 42.5"). Override the processed dataset with these exact values at the specified seconds. The audio overrides take precedence over both raw data and forward-filled data.

**Server Specifications:**
You must write a C program that performs (or loads the result of) this processing and then starts a TCP server with the following specifications:
- **Address:** `127.0.0.1`
- **Port:** `8888`
- **Protocol:** Raw TCP. 
- **Interaction:** 
  - A client will connect and send a 10-digit Unix timestamp (in seconds) followed by a newline (`\n`).
  - The server must respond with the cleaned float value for that timestamp, formatted to exactly 2 decimal places, followed by a newline (`\n`).
  - If the requested timestamp is completely outside the minimum or maximum range of the dataset, respond with `NOT_FOUND\n`.
  - The server should close the connection after sending the response, but remain running to accept further connections.

Compile your C code and leave the server running in the background. Do not exit your final script until the server is successfully listening on port 8888.