You are a compliance analyst tasked with generating an audit trail of attempted security exploits against our company's web infrastructure. 

We have a multi-service stack located in `/app/` that consists of:
1. An **Nginx** reverse proxy (listening on port 8080).
2. A **Flask** web application (running via gunicorn on port 5000).
3. A **Redis** server (port 6379) acting as an encrypted audit log message queue.

When the system is running, simulated clients send traffic and trigger Content Security Policy (CSP) violations. The Flask application receives these CSP violation reports, encrypts them using an obfuscated custom library located at `/app/crypto_logger.pyc` (compiled Python 3.10 bytecode), and pushes them to a Redis list named `csp_audit_logs`.

Your objectives are:
1. **Service Configuration:** Start the services using `/app/start.sh`. Ensure Nginx and Flask are correctly routed so that traffic to `http://localhost:8080/` reaches the Flask app, and the Flask app connects to Redis to dump logs. 
2. **Reverse Engineering:** Decompile or reverse engineer the `/app/crypto_logger.pyc` file to determine the encryption algorithm, key, and IV generation scheme used to encrypt the logs.
3. **Exploit Extraction (Data Processing):** Write a highly efficient Python script at `/home/user/processor.py` that continuously reads the encrypted logs from the Redis list `csp_audit_logs`, decrypts them, and parses the JSON CSP reports.
4. **Audit Generation:** From the decrypted CSP reports, isolate the XSS exploit payloads that caused the violations (often found embedded in the `document-uri` or `blocked-uri` parameters). Write the extracted payloads to `/home/user/audit_trail.jsonl`. 

Each line in `/home/user/audit_trail.jsonl` MUST be a valid JSON object with the exact following structure:
`{"timestamp": "<timestamp_from_csp_report>", "extracted_payload": "<the_raw_xss_string>"}`

Your `processor.py` script must process the logs accurately. You will be evaluated based on the **Payload Recovery Accuracy metric**, which measures how many of the true injected payloads you successfully decrypted and extracted without truncation or modification. 

Ensure your script runs and generates the `/home/user/audit_trail.jsonl` file. Do not stop the services once you are done; leave them running.