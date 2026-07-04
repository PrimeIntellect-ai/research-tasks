You are a data engineer tasked with building a real-time data processing middleware for legacy industrial sensors. The legacy sensors transmit corrupted, irregularly timed CSV telemetry data using outdated character encodings, and the data requires immediate cleaning, resampling, and proprietary calibration before being sent to our modern dashboards.

Your task is to build and start an HTTP web service listening on `127.0.0.1:8000`. You may use any programming language or framework you prefer (e.g., Python FastAPI/Flask, Node.js Express, Go).

**Service Requirements:**
1. **Endpoint:** Listen for HTTP POST requests on `/process`.
2. **Input Payload:** The body of the request will be raw bytes of a CSV file. 
    * The CSV is encoded in `Windows-1252` (CP1252). You must decode it properly.
    * The CSV has a header: `timestamp,sensor_id,raw_value`.
    * `timestamp` is in ISO 8601 format (e.g., `2024-01-01T10:00:00Z`).
    * `raw_value` is a float.
3. **Data Cleaning & Resampling:**
    * The incoming data often has gaps in time (skipped seconds). You must resample the data for each `sensor_id` to a strictly continuous **1-second** frequency.
    * The start and end time of the resampled series for a given sensor should exactly match the minimum and maximum timestamps present in the payload for that sensor.
4. **Interpolation:**
    * Resampling will introduce missing `raw_value` entries. 
    * The original data also occasionally contains empty fields for `raw_value` (e.g., `2024-01-01T10:00:02Z,A1,`).
    * You must fill all missing `raw_value`s using **linear interpolation** based on the timestamp.
5. **Rolling Statistics:**
    * Calculate a **5-second rolling average** of the interpolated `raw_value`s for each sensor.
    * The window should be closed on the right (include the current second and the 4 preceding seconds).
    * Use a minimum period of 1 (i.e., for the first 4 seconds, just average whatever is available).
6. **Proprietary Calibration (Black-Box):**
    * We have a proprietary legacy calibration tool located at `/app/calibrator` on your system. It is a stripped Linux binary.
    * For every row's rolling average, you must run this binary to get the final calibrated value.
    * Usage: `/app/calibrator <rolling_average_float>`
    * It prints the calibrated float to standard output. Since the binary is stripped, you can either call it as a subprocess for each row, or reverse-engineer its algorithm (it's a simple mathematical transformation) and implement it directly in your code to save overhead.
7. **Response:**
    * Return a JSON array of objects, sorted first by `sensor_id` (alphabetically), then by `timestamp` (chronologically).
    * Each object must have the format:
      ```json
      {
        "timestamp": "2024-01-01T10:00:00Z",
        "sensor_id": "A1",
        "calibrated_value": 42.512
      }
      ```
    * `calibrated_value` should be rounded to 3 decimal places.
    * Set the `Content-Type: application/json` header.

Start your server in the background or in a way that allows it to continue running while keeping the terminal available, as the automated system will send test requests to it once you indicate you are done.