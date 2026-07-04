As an automation specialist, you are tasked with building a robust data processing pipeline and a serving API for IoT sensor logs. You need to process a large text log file, handle data imputation, and serve the cleaned data securely.

Here are the requirements:

1. **Fix and Install the Vendored Library**:
   We use a third-party package called `parse` for structured text extraction. The source code for `parse` (version 1.19.0) has been pre-vendored at `/app/vendored/parse`. However, a junior developer made a breaking change in `/app/vendored/parse/parse.py` (specifically in the `search` method where it matches the string). You must find and fix this perturbation so the `parse.search()` function works correctly again. After fixing it, install the package in your environment.

2. **Data Processing Pipeline**:
   You are provided with a large log file at `/home/user/data/raw_sensors.log`. The file contains lines with mixed text and sensor readings, such as:
   `[2023-10-01T10:03:15] SYSTEM_LOG: Sensor TX-99 recorded a value of 45.2 at the edge node.`
   
   Write a Python script that streams this file (do not load the entire file into memory at once). Use the `parse` library to extract the timestamp, sensor ID, and the float value.
   
   Once extracted, for each unique sensor:
   - Round the timestamps down to the nearest minute.
   - Resample the time series to 1-minute intervals. If multiple readings fall in the same minute, average them.
   - There will be missing minutes (gaps) in the data. Fill these gaps using linear interpolation.
   - Perform stratified sampling on the interpolated data: for each hour, extract exactly 5 samples corresponding to the 0th, 12th, 24th, 36th, and 48th minute of that hour.

3. **HTTP API Service**:
   Implement and run an HTTP API service (using Flask, FastAPI, or similar) that listens on `127.0.0.1:8080`.
   - Implement a GET endpoint at `/api/v1/samples`.
   - It must accept a query parameter `sensor` (e.g., `?sensor=TX-99`).
   - It must require authentication via the header: `Authorization: Bearer secret_sensor_token_99X`. If missing or invalid, return a 401 status code.
   - It should return the processed, interpolated, and sampled data for the requested sensor as a JSON array of objects:
     `[{"timestamp": "2023-10-01T10:00:00", "value": 45.2}, {"timestamp": "2023-10-01T10:12:00", "value": 46.1}, ...]`
   - The timestamps in the JSON must be strings in ISO 8601 format (`YYYY-MM-DDTHH:MM:SS`). Values must be rounded to two decimal places.

Leave the server running in the background so it can be verified.