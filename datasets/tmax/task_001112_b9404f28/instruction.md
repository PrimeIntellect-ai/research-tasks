You are tasked with fixing and completing an ETL pipeline for sensor data. 

Currently, our bash-based data ingestion pipeline is silently dropping rows from our raw CSV dump because the `event_remarks` column contains embedded newlines. We also received an audio dictation containing critical calibration offsets that must be applied to the data before aggregation.

Your objectives:

1. **Robust CSV Parsing & DB Import:** 
   Read the raw data from `/app/raw_sensors.csv`. The CSV has the following columns: `timestamp`, `sensor_id`, `value`, `event_remarks`. Correctly parse the CSV (accounting for quoted embedded newlines) and load it into a SQLite database at `/home/user/sensors.db` in a table named `measurements`.

2. **Audio Transcription & Offset Application:**
   There is an audio file at `/app/calibration.wav`. It contains a voice dictation specifying the calibration offsets for the sensors. 
   - Transcribe the audio (you may install and use lightweight tools like `openai-whisper` or any suitable Python package via pip).
   - Extract the offsets (e.g., if the audio says "Sensor A offset is minus five", add -5 to all values for Sensor A).
   - Apply these offsets to the `value` column in your database.

3. **Windowed Aggregation:**
   Using Python or SQLite window functions, calculate a 3-hour rolling average of the corrected `value` for each `sensor_id`, ordered by `timestamp`.

4. **Template Generation:**
   Generate a final report at `/home/user/rolling_report.txt` using exactly this template format for each record, sorted chronologically, then by sensor_id:
   `[<timestamp>] Sensor <sensor_id> Rolling Avg: <rolling_avg_rounded_to_2_decimals>`

You must complete the entire process using standard terminal tools and Python. Be sure your CSV parsing doesn't drop any of the valid rows with embedded newlines.