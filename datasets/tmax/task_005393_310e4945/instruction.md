You are a localization engineer managing an automated translation and metrics pipeline. A critical regional server experienced an outage, and the local technicians left an automated voice memo with the missing telemetry data. You need to build a Python ETL pipeline that extracts this audio data, integrates it with our historical metrics, detects anomalies, and serves the finalized translated data via a secure API.

Here are your instructions:

1. **Audio Transcription & Extraction:**
   There is an audio artifact located at `/app/telemetry_alert.wav`. Use a Python-based tool or library (like `SpeechRecognition` or `whisper`) to transcribe the audio. The audio contains spoken timestamps and metric values in the format: "Timestamp [unix_time], value [metric_value]". Extract these pairs into a structured format.

2. **Data Reshaping (Wide to Long):**
   You are provided with a historical dataset at `/app/system_metrics.csv`. It is currently in a wide format: `timestamp, server_A_metric, server_B_metric, server_C_metric`.
   Transform this dataset into a long format with columns: `timestamp`, `server_name`, and `metric_value`. 
   
3. **Pipeline Integration & Quality Gates:**
   Merge your transcribed audio data into the long-format dataset. Assign the transcribed data to `server_name = "server_regional_1"`. 
   Sort the entire combined dataset chronologically by `timestamp`, then group by `server_name`.

4. **Anomaly & Changepoint Detection:**
   Implement a processing step to flag anomalies. An anomaly is defined as any `metric_value` strictly greater than `90.0`.

5. **Service Orchestration:**
   Create and start a Python-based HTTP web service (e.g., using FastAPI or Flask) that exposes this processed data.
   - **Host/Port:** The service must listen on `0.0.0.0:8080`.
   - **Endpoint:** `GET /api/v1/anomalies`
   - **Authentication:** The endpoint must enforce Bearer token authentication. Clients must provide the header: `Authorization: Bearer l10n-metrics-secret`
   - **Payload Format:** The endpoint must return a JSON object with a single key `"anomalies"` containing a list of objects, each with `"timestamp"`, `"server_name"`, and `"metric_value"`, sorted by timestamp ascending.

Ensure the service is left running in the background so our automated verifier can query it.