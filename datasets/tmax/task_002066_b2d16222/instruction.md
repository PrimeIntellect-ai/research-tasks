You are tasked with a multi-stage data processing and API integration workflow. You must process an audio-recorded telemetry log, transform the extracted time series, and serve it via a C++ HTTP service.

**Background:**
A field technician recorded some missing sensor telemetry via an audio log because the primary datalogger failed. You must transcribe this audio, extract the time series, process it against a baseline, and serve the results securely.

**Step 1: Transcription**
You are provided an audio file at `/app/sensor_log.wav`. It contains spoken telemetry data in English. The speech contains an Operator ID and a sequence of timestamp-value pairs (e.g., "Operator ID 1234. Second 0, value 10.0. Second 20, value 15.0...").
Use an appropriate tool (e.g., downloading and compiling `whisper.cpp` or using Python's `speech_recognition` module locally) to transcribe this audio into text.

**Step 2: C++ Time Series Processing Server**
Write a C++ application (you may use a lightweight single-header library like `httplib.h` which you can download) that does the following:
1. **Data Parsing & Validation:** Parse the transcribed text to extract the Operator ID and the timestamped values. Discard any values that are negative or greater than 100.0.
2. **Data Masking:** Mask the Operator ID so that it is replaced by the string `"MASKED"`.
3. **Resampling:** The telemetry should have a reading every 10 seconds. Identify missing 10-second intervals (e.g., if you have data for 0 and 20, 10 is missing) and gap-fill using simple linear interpolation.
4. **Similarity Computation:** Read a baseline CSV file located at `/app/baseline.csv`. Both the resampled data and the baseline data will now have matching timestamps. Compute the Mean Absolute Error (MAE) between the resampled telemetry values and the baseline values.

**Step 3: Service Deployment**
Your C++ application must start an HTTP server listening on `0.0.0.0:8080`.
The server must implement two endpoints, both requiring an `Authorization: Bearer secret_ts_2024` header. If the header is missing or incorrect, return a `401 Unauthorized`.

*   `GET /api/telemetry`
    Returns a JSON response representing the processed data:
    ```json
    {
      "operator": "MASKED",
      "data": [
         {"time": 0, "value": 10.0},
         {"time": 10, "value": 12.5}
      ]
    }
    ```
*   `GET /api/mae`
    Returns a JSON response with the computed MAE:
    ```json
    {
      "mae": 1.25
    }
    ```

**Requirements:**
- Do not require root access. Install libraries locally or use downloaded header files.
- Compile your C++ server and leave it running in the background. Write a script `run_server.sh` in `/home/user/` that compiles and runs your server. Execute it before finishing.