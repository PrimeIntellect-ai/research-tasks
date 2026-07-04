You are tasked with fixing and completing a data ingestion pipeline that processes CSV files uploaded by users. 

Currently, the system is partially implemented in `/app/`. It consists of three services:
1. **Nginx** (listening on port 8080) acts as an ingress proxy.
2. **Flask API** (listening on port 5000) receives CSV uploads via Nginx and pushes the file paths to a Redis queue.
3. **Redis** (listening on port 6379) acts as the message broker.

Your tasks are as follows:

**1. Service Reconfiguration**
The Nginx ingress is failing to accept CSV uploads larger than 1MB (returning a 413 Payload Too Large error). You must reconfigure Nginx to accept file uploads up to 20MB and ensure the Nginx service is restarted/reloaded so the new configuration takes effect. The Nginx config is located at `/app/nginx/nginx.conf`.

**2. Develop the Data Sanitizer / Worker**
The system is missing the worker process that consumes data. You must write an executable CLI tool located exactly at `/home/user/csv_sanitizer`. You may write this in any language you prefer (Python, Node, Bash + jq, etc.). 

This tool will be invoked as follows:
`/home/user/csv_sanitizer <input_csv_path> <output_json_path>`

Your `csv_sanitizer` must adhere strictly to these processing rules:
* **Validation & Security (Filter):** It must scan the CSV for "CSV Injection" attacks. If any field in the CSV begins with `=`, `+`, `-`, or `@` AND the entire file contains malicious payloads (for the sake of this pipeline, reject ANY file where a field starts with one of those four characters), the script MUST exit with a non-zero exit code (e.g., 1) and not create the output file.
* **Robust Parsing:** The tool must correctly parse standard CSV files, explicitly handling fields that contain embedded newlines (`\n`) and escaped commas. Naive line-by-line splitting will corrupt the data.
* **Deduplication:** Generate a SHA-256 hash of each parsed row's raw string values (concatenated in order). Deduplicate the rows based on this hash. Keep only the first occurrence of each row.
* **Feature Extraction & Formatting:** For valid files, extract only the columns named `user_id`, `timestamp`, and `transaction_amount` (ignore other columns). Write the deduplicated, extracted records to `<output_json_path>` as a JSON array of objects.
* **Success:** If the file is valid and successfully processed, the script must exit with code `0`.

**3. End-to-End Test**
Ensure all services are running and your sanitizer works. A test script `/app/start_services.sh` is available to boot Nginx, Flask, and Redis.

Ensure `/home/user/csv_sanitizer` is executable (`chmod +x`). Do not modify the Flask app code itself, only provide the worker tool and fix Nginx.