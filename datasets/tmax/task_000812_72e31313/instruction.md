You are tasked with building a Configuration Tracking and Resampling API. We have a set of baseline service configurations and a log of configuration changes. You need to reconstruct the historical state of these configurations and expose them via a secure API.

Here are the specific requirements:

1. **Extract API Credentials:**
   There is an image file located at `/app/auth_spec.png`. Use OCR (e.g., `tesseract`, which is installed) to read this image. It contains the exact port number your API must listen on and a secret authentication token.

2. **Process Configuration Data:**
   - **Base State:** A CSV file at `/app/data/base.csv` contains the initial state for various services (columns: `service`, `cpu`, `mem`). Assume this state applies from `2024-01-01T00:00:00`.
   - **Changes Log:** A JSON-lines file at `/app/data/changes.jsonl` contains subsequent configuration changes (fields: `time`, `service`, `cpu`, `mem`, `note`). 
   - *Warning:* The system that generated `changes.jsonl` sometimes outputs corrupted Unicode escape sequences in the `note` field (e.g., `\uZZZZ`), which will break standard JSON parsers. You must gracefully handle or sanitize these lines to extract the valid configuration fields.

3. **Validation and Resampling:**
   - **Validation Constraints:** If any change event requests `cpu < 1` or `mem < 128`, that specific event is invalid and must be completely ignored.
   - **Resampling / Gap-filling:** Reconstruct the state of all services over time using a forward-fill strategy. A service's configuration remains constant until a valid change event updates it.

4. **API Service:**
   Write and start a Python HTTP service (e.g., using Flask, FastAPI, or `http.server`) listening on `127.0.0.1` at the **Port** extracted from the image.
   - The API must enforce authentication. Clients must provide an `X-Auth-Token` HTTP header matching the **Token** extracted from the image. Return a `401 Unauthorized` status otherwise.
   - Implement an endpoint `GET /api/state?time=YYYY-MM-DDTHH:MM:SS`.
   - The endpoint must return the exact active configuration for all services at the requested timestamp (e.g., a JSON dictionary where keys are service names and values are dictionaries with `cpu` and `mem` integers).

5. **Cron Management:**
   Write a valid cron job configuration line to `/app/backup.cron` that schedules a hypothetical script (`/app/backup.sh`) to run every day at 2:00 AM.

Leave the Python API server running in the background so it can be tested.