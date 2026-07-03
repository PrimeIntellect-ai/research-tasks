You are acting as a backup operator restoring data from a legacy system. We have successfully restored the data files, but to verify their integrity, we must apply a specific legacy cryptographic transformation to the headers of the restored files. Unfortunately, the exact algorithm was lost, save for a scanned page of the original operator runbook located at `/app/runbook_scan.png`.

Your objectives are to implement the verification logic, expose it via a secure local web service for the automated restore systems to consume, and set up proper logging and health monitoring.

Step 1: Extract the Verification Algorithm
Use OCR tools (e.g., `tesseract` is preinstalled) to read the contents of `/app/runbook_scan.png`. Extract the specific string transformation algorithm described in the text.

Step 2: Implement the Verifier
Write a Python script at `/home/user/verify_header.py`. This script must accept exactly one string as a command-line argument, apply the transformation algorithm you extracted from the runbook scan, and print the resulting string to standard output. 
*Note:* This script will be rigorously fuzzed against a reference implementation to ensure bit-exact output equivalence, so your implementation must exactly match the logic described in the image.

Step 3: Setup Secure Web Server & Health Check
Create a Python-based HTTPS server script at `/home/user/backup_server.py`.
- It must listen on `127.0.0.1:8443`.
- Generate self-signed TLS certificates and store them in `/home/user/certs/cert.pem` and `/home/user/certs/key.pem`.
- Endpoint `/health`: Must return an HTTP 200 status with the JSON body `{"status": "ok"}`.
- Endpoint `/verify`: Must accept a GET request with a query parameter `?data=...`. It should apply the algorithm from Step 2 to the `data` value and return the transformed string.
- Every time `/verify` is hit, append a log entry to `/home/user/logs/restore.log` in the format: `[YYYY-MM-DD HH:MM:SS] VERIFY: <original_data> -> <transformed_data>`. (Create the `/home/user/logs/` directory if it does not exist).

Step 4: Log Rotation
Write a Python script at `/home/user/rotate_logs.py` that performs log rotation for `/home/user/logs/restore.log`. When executed, it should:
- Shift `restore.log.2` to `restore.log.3` (if it exists).
- Shift `restore.log.1` to `restore.log.2` (if it exists).
- Move `restore.log` to `restore.log.1`.
- Create a new, empty `restore.log`.
Discard any logs older than `.3`.

Complete these tasks. You may start the web server in the background once configured.