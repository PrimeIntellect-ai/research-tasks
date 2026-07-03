You are a security engineer tasked with rotating a compromised credential in a legacy Go web service. The old credential was hardcoded and leaked via debug headers and access logs.

Your objective is to complete the credential rotation and secure the service by performing the following steps:

1. **Credential Creation & File Permissions:**
   Create a directory `/home/user/secrets`.
   Inside it, create a file named `/home/user/secrets/api.key` containing exactly the string `987654321-NEW-SECRET`.
   Secure this file by setting its permissions to `0400` (read-only for the owner, no permissions for anyone else).

2. **Source Code Modification:**
   The source code for the service is located at `/home/user/legacy-svc/main.go`. Modify it to achieve the following:
   * **Remove Hardcoded Secret:** Make the service read its secret from `/home/user/secrets/api.key` at startup instead of using the hardcoded `OLD_SECRET`.
   * **Authentication:** Update the `/auth` endpoint to validate the `Authorization` header against the new secret. If it matches, return HTTP 200 with the body `OK`. If not, return HTTP 401.
   * **Header Inspection & Removal:** The service currently reflects the `X-Debug-Token` header in its responses. Modify the code to ensure the `X-Debug-Token` header is *never* sent back in any HTTP response.
   * **Sensitive Data Redaction:** The service writes access logs to `/home/user/legacy-svc/app.log`. Update the logging middleware so that if the new secret (`987654321-NEW-SECRET`) ever appears in the log string (e.g., if someone sends it in a URL or user-agent), it is completely replaced with the exact string `[REDACTED]` before being written to the log file.

3. **Build and Run:**
   * Build the Go application: compile `/home/user/legacy-svc/main.go` into an executable at `/home/user/legacy-svc/server`.
   * Start the server in the background so it listens on `127.0.0.1:8080`.

4. **Completion:**
   Once the server is running and configured correctly, create a file named `/home/user/rotation_report.txt` containing the word `DONE`.

Note: You may install any standard Go packages if needed, but the standard library is sufficient. Ensure the server is actively running on port 8080 before creating the report file.