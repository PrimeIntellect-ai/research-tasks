You are acting as a DevSecOps engineer implementing a Policy-as-Code service. You need to create a Python HTTP API that enforces security policies by analyzing server logs, verifying file integrity, and requiring a specific authorization token extracted from a badge image.

Your task is to build a Python-based web service (you can use Flask, FastAPI, or Python's built-in `http.server`) that listens on `0.0.0.0:8080`.

Here are the requirements for the service:

1. **Authentication Token**: 
   The service must require an `Authorization: Bearer <TOKEN>` header for all requests to the `/policy-check` endpoint. The `<TOKEN>` must exactly match the text found in the image located at `/app/auth_badge.png`. You will need to extract this text using OCR (e.g., using `tesseract`). If the header is missing or the token is incorrect, the service must return an HTTP `401 Unauthorized` status.

2. **Endpoint Specification**:
   - **Method**: `POST`
   - **Path**: `/policy-check`
   - **Payload**: JSON containing two keys: `"user"` and `"script_name"`. Example: `{"user": "alice", "script_name": "deploy.sh"}`

3. **Policy Rules**:
   When a valid request is received, the service must evaluate the following policies in order:
   
   - **Privilege Escalation Audit**: 
     Parse the log file located at `/app/auth.log`. If the requested `"user"` has any logged entry indicating a failed `sudo` attempt (specifically, lines containing `command not allowed` for that user), the service must return an HTTP 200 response with the JSON:
     `{"status": "deny", "reason": "escalation_attempt"}`
   
   - **Integrity Check (Cryptographic Hashing)**:
     If the user passes the privilege audit, verify the SHA-256 checksum of the script located at `/app/scripts/<script_name>`. Compare its actual SHA-256 hash against the expected hash listed in `/app/manifest.sha256`. 
     If the file does not exist, the hash does not match, or the file is not listed in the manifest, return an HTTP 200 response with the JSON:
     `{"status": "deny", "reason": "checksum_mismatch"}`
     
   - **Allow**:
     If the user has no failed sudo attempts and the script's checksum exactly matches the manifest, return an HTTP 200 response with the JSON:
     `{"status": "allow"}`

Ensure your service stays running in the foreground or background so that it can be tested. You may install any necessary Python packages (like `flask`, `fastapi`, `pytesseract`, `uvicorn`) using `pip`.