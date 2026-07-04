You are a compliance analyst tasked with generating an audit trail for an internal web application running locally on `http://127.0.0.1:8080`. You need to test its authentication flow, inspect its session management security, verify the integrity of the data it serves, and ensure your audit tools run in a sandboxed environment to prevent accidental host modification.

Perform the following steps:

1. Write a Python script at `/home/user/audit.py` that does the following:
   - Sends a POST request to `http://127.0.0.1:8080/login` with the JSON payload: `{"user": "auditor", "pass": "audit123"}`.
   - Inspects the response headers to extract the `session_token` cookie.
   - Analyzes the `Set-Cookie` header to determine if the `HttpOnly` security flag is present.
   - Uses the extracted `session_token` cookie to send an authenticated GET request to `http://127.0.0.1:8080/secure_data.txt`.
   - Computes the SHA-256 hash of the exact body content of `secure_data.txt`.
   - Writes the findings to `/home/user/audit_trail.json` strictly in the following JSON format:
     ```json
     {
       "httponly_flag_present": false,
       "file_sha256": "<computed_sha256_hash_here>"
     }
     ```
     *(Set the boolean to true or false depending on your findings).*

2. To ensure the audit script cannot accidentally modify host files, write a shell script at `/home/user/run_isolated.sh` that executes `/home/user/audit.py` using `bwrap` (Bubblewrap) with the following exact restrictions:
   - Provide read-only access to the entire root filesystem (`/`).
   - Provide read-write access **only** to the file `/home/user/audit_trail.json` (you may need to create an empty file first so bwrap can bind it).
   - Drop all other namespaces but share the network namespace (`--share-net`) so the script can reach localhost.
   - Start the script using `/usr/bin/python3`.

3. Execute your Python script to generate the `/home/user/audit_trail.json` file. *(Note: If `bwrap` execution fails in your containerized environment due to user namespace restrictions, you are allowed to run `/usr/bin/python3 /home/user/audit.py` directly to generate the JSON file. However, `run_isolated.sh` MUST contain the correctly formatted `bwrap` command).*

Ensure both scripts are saved and the `audit_trail.json` file is successfully created with the correct data.