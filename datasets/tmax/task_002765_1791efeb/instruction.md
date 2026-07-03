As a localization engineer, you are tasked with fixing and updating our automated translation ingestion pipeline. Recently, some third-party translation vendors have been submitting localization files (JSON and CSV) that contain anomalous data, such as extremely long corrupted strings or malicious script tags. 

You need to resolve two major issues to get the pipeline fully operational and secure.

**Part 1: Pipeline Orchestration & Service Configuration**
Our translation pipeline involves three services located in `/app/`:
1. Nginx (proxying requests on port 8080)
2. A Flask translation API (`/app/api.py`, running on port 5000)
3. A Redis cache (running on port 6379)

Currently, the services are not communicating correctly. You need to:
- Edit `/app/nginx/nginx.conf` so that any request to `http://localhost:8080/ingest` is correctly proxied to the Flask API at `http://127.0.0.1:5000/ingest`.
- Update `/app/.env` so the Flask app can connect to Redis. The variable `REDIS_HOST` is currently pointing to a dead external server; change it to `127.0.0.1`.
- Restart or reload the services as necessary using the provided `/app/restart_services.sh` script.

**Part 2: Translation Anomaly Detector**
The Flask API uses an external script to validate translation files. You must implement this script at `/home/user/validate_loc.py`.

The script must accept two arguments:
`python3 /home/user/validate_loc.py <input_file> <output_file>`

The script must do the following:
1. **Multi-format reading:** Parse the input file, which will be either a flattened JSON key-value object (`{"key": "translation"}`) or a CSV with columns `key,translation`.
2. **Anomaly detection via summary statistics:** Compute the mean and standard deviation of the lengths of all translation values in the file. 
3. **Filtering Rules:** Reject the file (do not write to output, exit with code 1) if:
    - Any individual translation string's length is strictly greater than `mean + 3 * std_dev`.
    - Any translation string contains the substring `<script>` or `${`.
4. **Acceptance:** If the file passes these checks, write the parsed translations out as a valid JSON object to `<output_file>` and exit with code 0.

Once complete, verify that you can send a valid JSON file to `http://localhost:8080/ingest` via POST (using the `-F "file=@<path>"` curl format) and receive a 200 OK, while bad files return a 400 error.