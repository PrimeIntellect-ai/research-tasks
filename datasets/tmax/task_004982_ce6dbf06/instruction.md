You are a security engineer tasked with rotating credentials for a legacy webhook service. The source code for this service has been lost, and the service currently relies on a hardcoded, compromised authentication token. 

Your objective is to extract the compromised token, isolate the legacy binary, and implement a secure Python proxy that enforces a new rotated token.

Here are the specific requirements:

1. **ELF Analysis**: You have been provided with a compiled executable at `/home/user/legacy_worker`. Analyze this binary to find the hardcoded authentication token it expects. The binary processes HTTP GET requests and checks for an `Authorization: Bearer <token>` header.

2. **Process Isolation and Proxying**: Write a Python script at `/home/user/secure_proxy.py` using only the standard library. The script must:
   - Launch `/home/user/legacy_worker 8080` as a background subprocess, ensuring it binds to local port 8080.
   - Start an HTTP server listening on `127.0.0.1` port `9090`.
   - Require a new rotated credential in incoming requests: `Authorization: Bearer ROTATED_TOKEN_2024`.
   - If the new credential is provided, strip it, inject the *legacy* token you extracted in step 1, and proxy the request to the legacy worker on port 8080. Return the worker's response to the client.
   - If the new credential is not provided or is incorrect, return an HTTP 403 Forbidden response without forwarding the request.

3. **Service Auditing**: After verifying your proxy is running, write an audit script or manually test the setup. You must create a file at `/home/user/audit_report.txt` containing exactly three lines in the following format:
   - Line 1: The extracted legacy token. (Format: `LEGACY_TOKEN=<token>`)
   - Line 2: The HTTP status code returned by the proxy on port 9090 when using the correct new token `ROTATED_TOKEN_2024`. (Format: `PROXY_VALID=<status_code>`)
   - Line 3: The HTTP status code returned by the proxy on port 9090 when using an invalid token. (Format: `PROXY_INVALID=<status_code>`)

Ensure that the background `legacy_worker` process and your proxy are running when you consider the task complete, so they can be verified.