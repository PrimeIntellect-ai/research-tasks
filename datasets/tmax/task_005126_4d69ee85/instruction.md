I need you to help me organize a complex dataset of sensor readings and serve it via a local API.

The raw data is located in `/home/user/raw_data/`, spread across multiple nested subdirectories. The data comes in four different formats:
1. **CSV files (`*.csv`)**: These have columns `date, time, sensor, reading`. The timestamp should be combined as `YYYY-MM-DDTHH:MM:SS`.
2. **JSON files (`*.json`)**: These contain arrays of objects like `{"ts": "YYYY-MM-DDTHH:MM:SS", "sensor_id": "...", "val": 12.3}`.
3. **Log files (`*.log`)**: These are multi-line text records. Each record starts with `---RECORD---`, followed by lines for `TS: <timestamp>`, `ID: <sensor_id>`, `VAL: <value>`, and ends with `---END---`.
4. **Binary files (`*.dat`)**: These are in a legacy proprietary format. There is an undocumented, stripped binary at `/app/sensor_decoder` that was previously used to parse these files. You will need to figure out how to invoke it to extract the data (it outputs JSON).

Your task is to:
1. Write a Bash-based data processing pipeline (using `jq`, `awk`, `find`, etc.) that recursively traverses `/home/user/raw_data/`, parses all these files, and unifies the data into a single consolidated format.
2. Build and start a web service listening on `127.0.0.1:8080`. You may use Python to write the web service, but the data processing must be heavily Bash-driven.
3. The web service must expose an endpoint: `GET /query?sensor=<sensor_id>`.
4. The endpoint must return a JSON array of all readings for the requested `<sensor_id>`, with each object formatted exactly as: `{"timestamp": "YYYY-MM-DDTHH:MM:SS", "value": <numeric_value>}`. The array must be sorted chronologically by timestamp (oldest to newest).
5. The web service must enforce authentication. It should only accept requests that include the HTTP header `Authorization: Bearer RES-992`. If the header is missing or incorrect, return a `401 Unauthorized` status. If the sensor is not found in the data, return an empty JSON array `[]` with a `200 OK` status.

Please leave the service running in the background listening on port 8080.