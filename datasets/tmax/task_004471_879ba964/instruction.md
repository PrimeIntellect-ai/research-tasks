You are a data engineer tasked with building an ETL pipeline that processes real-time IoT weather station telemetry. The system receives batches of sensor data combined with multilingual operator notes, but the data is messy, contains missing values, and is currently under a data-poisoning attack where malicious actors are injecting invalid payloads using Unicode exploits.

Your task is to write a Python script `/home/user/etl_worker.py` that processes a directory of incoming JSON batch files, sanitizes them, and forwards the clean data to a downstream API.

### Environment & Services
Multiple cooperating services manage the pipeline's lifecycle. A startup script is provided to spin them up.
1. Start the backend services by running: `/bin/bash /app/start_services.sh`
2. This will start:
   - A Redis broker on `localhost:6379` (used internally by the backend).
   - An Ingestion Webhook (Flask) on `http://localhost:8080/ingest`.

### Data Format
The incoming data is located in `/home/user/incoming/` as `.json` files. Each file contains a JSON array of telemetry objects:
```json
[
  {
    "station_id": "ST-01",
    "timestamp": 1690000100,
    "temperature": 22.5,
    "humidity": null,
    "note": "Système normal 異常なし"
  }
]
```

### Processing Requirements

You must implement a function `process_payload(batch: list[dict]) -> list[dict]` in `/home/user/etl_worker.py` (which you must also make executable to process the files in `/home/user/incoming/` and POST to the webhook).

**1. Interpolation & Imputation:**
The `temperature` and `humidity` fields may occasionally be `null`. 
- You must impute missing values using linear interpolation based on the timestamp, using the nearest available past and future records for the *same* `station_id` within the *same* batch.
- If a value cannot be interpolated (e.g., missing at the very beginning or end of a batch with no bounding values), drop the record.

**2. Constraint-Based Validation:**
After imputation, enforce the following physical constraints. If a record violates these, drop the record entirely:
- `temperature` must be between `-50.0` and `60.0` (inclusive).
- `humidity` must be between `0.0` and `100.0` (inclusive).

**3. Unicode Text Processing (Adversarial Defense):**
The `note` field contains multilingual text (French, Japanese, Arabic, etc.). However, it is being targeted by malicious payloads. You must analyze the `note` string and DROP the entire record if the `note` violates any of these security constraints:
- **No Zalgo text:** Reject the record if any base character has more than 2 combining marks (Unicode category `Mn` or `Me`).
- **No BiDi overrides:** Reject the record if it contains any Unicode bidirectional formatting control characters (e.g., U+202E, U+202D, U+202A, U+202B, U+202C).
- *Valid multi-language text must be preserved.* Do not indiscriminately strip non-ASCII characters.

### Integration
For every JSON file in `/home/user/incoming/`:
1. Parse the JSON.
2. Pass the list of dicts through your `process_payload()` logic to filter and impute.
3. Send the resulting sanitized list as a JSON payload via a `POST` request to `http://localhost:8080/ingest` with `Content-Type: application/json`.

Ensure your script is robust and cleanly handles the processing rules. Our automated test suite will independently import your `process_payload` function and test it against a hidden adversarial corpus to ensure 100% of malicious records are rejected and 100% of valid records are preserved.