You are tasked with fixing and completing a real-time data cleaning pipeline for our analytics team. The system receives streaming user profile data, validates it, and writes it to a central database. 

Currently, the system is broken and incomplete. You must implement the constraint-based data validation, fix the service configuration to properly orchestrate the flow, and ensure the pipeline correctly sanitizes adversarial inputs.

### System Architecture
The system consists of three cooperating services started via `/app/start_services.sh` (which you should use to restart/test the system):
1. **Nginx (Port 8000)**: Acts as the entry point, proxying requests to the ingestion API.
2. **Flask Ingestion API (Port 5000)**: Defined in `/app/ingest.py`. It receives JSON payloads from Nginx, validates them, and sends valid ones to the database writer.
3. **Database Writer (UNIX Socket `/tmp/db.sock`)**: A background process (`/app/db_writer.py`) that accepts valid JSON strings over a UNIX socket and performs bulk inserts into a SQLite database at `/app/analytics.db`.

### Your Objectives

**1. Create the Data Sanitizer (`/home/user/sanitizer.py`)**
You must write a Python script that acts as our validation filter. The script should take a JSON string as a command-line argument, validate it, and exit with code `0` if the data is completely valid, or exit with code `1` if it violates ANY constraint.
The JSON payload contains user profiles with the following strict constraints:
- `user_id`: Must be a valid UUIDv4.
- `username`: Must be exactly 3 to 20 characters long, containing only alphanumeric characters (regex required).
- `email`: Must be a valid email format.
- `age`: Must be an integer strictly between 18 and 120 (inclusive).
- `bio`: Must NOT contain any HTML-like tags (e.g., `<script>`, `<b>`, `</a>`). Construct a regex to reject any string containing `<` followed by any characters and `>`.

**2. Fix the Service Configuration**
- The Flask app (`/app/ingest.py`) currently has a placeholder function `validate_payload(json_str)`. Modify it to execute your `/home/user/sanitizer.py` as a subprocess. If the script exits with `0`, the data should be forwarded to the DB.
- The Flask app is failing to send data to the DB Writer. Inspect `/app/ingest.py` and fix the UNIX socket connection logic so it successfully transmits valid payloads to `/tmp/db.sock`.
- Nginx (`/etc/nginx/sites-enabled/default` or similar local config provided at `/app/nginx.conf`) might be misconfigured. Ensure Nginx correctly forwards POST requests on `http://localhost:8000/submit` to the Flask app on port 5000.

**3. Integration & Testing**
To verify your setup, you must process the corpora provided in `/app/corpora/`.
- `/app/corpora/clean/`: Contains 100 perfectly valid JSON files.
- `/app/corpora/evil/`: Contains 100 invalid, malicious, or malformed JSON files.

Once your system is running, simulate the data stream by writing a bash loop to `POST` all 200 files in the corpora to `http://localhost:8000/submit` via `curl`. 
When finished, the database `/app/analytics.db` should contain exactly 100 rows, originating ONLY from the clean corpus. Create a log file at `/home/user/pipeline_status.log` containing the exact count of rows in the SQLite database to prove completion.