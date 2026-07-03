You are a log analyst investigating a sophisticated cyber incident. The attackers attempted to obfuscate their tracks by altering log encodings and injecting duplicate entries. 

You must complete the following investigation and remediation pipeline:

1. **Extract Encoding Key**: The attackers left a screenshot of their configuration tool at `/app/evidence.png`. Use OCR (e.g., `tesseract`) to read the image. It contains a string like `TargetEncoding: <encoding_name>`. Extract this encoding name.
2. **Decode and Cleanse Logs**: Read the raw binary log file located at `/home/user/raw_logs.dat`. Decode it using the encoding extracted from the image. Each line is a pipe-separated string: `timestamp|ip_address|message`.
3. **Hash-based Deduplication**: Multiple duplicate entries exist. Deduplicate the logs by computing an MD5 hash of the `timestamp` and `ip_address` combined (e.g., `md5(timestamp + ip_address)`). Keep only the first occurrence of each hash.
4. **Feature Extraction & Joining**: 
    - Extract a numeric `error_code` from the `message` field (look for the pattern `ErrCode:[0-9]+`).
    - Join the deduplicated logs with the IP lookup table at `/home/user/ip_map.csv` (headers: `ip_address,department`) based on the `ip_address`.
5. **Serve the Results**: To integrate with our SOC dashboard, write a Python script that starts an HTTP server on `127.0.0.1:9090`. 
    - Endpoint: `GET /api/threats`
    - Query Parameter: `?dept=<department_name>`
    - Response: A JSON array of objects for the matching department. Each object must have keys: `timestamp`, `ip_address`, `department`, `error_code`, `message`. 
    - The HTTP server must require a Bearer token in the Authorization header: `Bearer SOC-Analyst-2024`. Reject unauthorized requests with a 401.

Ensure the server remains running in the background so the automated verification system can query it.