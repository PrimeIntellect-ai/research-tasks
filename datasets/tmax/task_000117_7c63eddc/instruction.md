You are a data analyst at a smart grid company. You have been given a set of raw energy consumption CSV files and need to process them, calibrate the data, perform time-based aggregations, and expose the results via a RESTful API.

Here are your instructions:

1. **Extract the Calibration Factor:**
   There is an image containing calibration specifications at `/app/config/specs.png`. Use OCR (e.g., `tesseract`, which is installed on the system) to extract the text. You are looking for a line that contains the calibration multiplier in the format `MULTIPLIER=<number>`. Extract this floating-point number.

2. **Process Time Series Data:**
   In the directory `/app/input/`, you will find several CSV files (e.g., `sensor_A.csv`, `sensor_B.csv`). 
   Each file contains two columns: `ts` (an ISO8601 timestamp string) and `val` (a raw float value). 
   For each file:
   - Read the CSV.
   - Multiply all `val` entries by the calibration multiplier you extracted from the image.
   - Set the `ts` column as a datetime index.
   - Perform a windowed aggregation: Resample the calibrated data into 1-hour rolling/fixed bins (e.g., `1H` frequency) calculating the *mean* for each bin. Use the start of the hour for the bin label.

3. **Database Export:**
   Save the aggregated data into a SQLite database located at `/app/db/timeseries.sqlite3`.
   Create a table named `hourly_data` with the following schema:
   - `sensor_id` (TEXT) - The name of the sensor (e.g., "sensor_A", derived from the filename).
   - `hour_ts` (TEXT) - The timestamp of the hour bin in ISO8601 format (e.g., `2024-01-01T12:00:00`).
   - `avg_val` (REAL) - The resampled average calibrated value.

4. **Serve Data via API:**
   Write and start a Python web server (using Flask, FastAPI, or Python's built-in `http.server`) that serves this database.
   - **Listen address:** `127.0.0.1:8000`
   - **Endpoint:** GET `/data`
   - **Query Parameter:** `sensor_id` (e.g., `/data?sensor_id=sensor_A`)
   - **Authentication:** The API MUST require an HTTP `Authorization` header with the exact value: `Bearer ops_token_99`. If the token is missing or incorrect, return a 401 Unauthorized status code.
   - **Response Format:** A JSON array of objects, sorted chronologically by `hour_ts`, e.g.,
     `[{"hour_ts": "2024-01-01T12:00:00", "avg_val": 150.5}, ...]`

You must keep the server running in the background or foreground so that it can be tested. Ensure the database directory exists before creating the SQLite file.