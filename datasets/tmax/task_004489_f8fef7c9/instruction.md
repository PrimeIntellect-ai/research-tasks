You are an automation specialist responsible for creating a robust time-series data ingestion pipeline for industrial IoT sensors. You need to build a validation script that filters out malformed or physically impossible telemetry data before it enters our time-series database. 

We have a mock remote server that serves the latest batch of sensor payloads. You need to download the data, extract the validation constraints from a physical sensor label, and write a Python validation script.

Here are the specific steps:

1. **Local-Remote Transfer Pipeline**:
   Start the local data server by executing `/app/start_server.sh` in the background. It will serve an archive at `http://127.0.0.1:8080/data.tar.gz`. Download this archive and extract it to `/home/user/data/`. You will find two directories: `clean/` and `evil/`.

2. **Constraint Extraction (Image)**:
   There is an image of the sensor's calibration label at `/app/sensor_label.png`. You must read this image (using OCR tools like `tesseract`, which is preinstalled) to find two critical pieces of information:
   - The **Calibration Epoch** (a UTC ISO 8601 timestamp).
   - The **Max RPM** (a floating-point number).

3. **Time-Series Validator Implementation**:
   Write a Python script at `/home/user/validate.py` that takes a single file path as a command-line argument:
   `python3 /home/user/validate.py <path_to_json_file>`

   The script must parse the JSON file and validate it against the following rules:
   - It must be valid JSON containing at least the fields `timestamp` (string) and `rpm` (numeric).
   - The `timestamp` field must be a valid ISO 8601 string (it may be in various timezones, e.g., `Z`, `+02:00`, `-05:00`).
   - **Timestamp Alignment**: You must parse and convert the timestamp to UTC. The resulting UTC time must be strictly greater than or equal to the **Calibration Epoch** extracted from the image.
   - The `rpm` value must be greater than or equal to `0.0` and strictly less than or equal to the **Max RPM** extracted from the image.
   
   If ALL rules are satisfied, the script MUST exit with status code `0` (Success).
   If ANY rule is violated (or if the file is missing/unreadable), the script MUST exit with status code `1` (Failure).

Your goal is to ensure your script at `/home/user/validate.py` perfectly classifies the downloaded corpora: it must exit `0` for 100% of the files in `/home/user/data/clean/` and exit `1` for 100% of the files in `/home/user/data/evil/`.