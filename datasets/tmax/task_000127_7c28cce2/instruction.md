You are a security engineer responding to an incident. We suspect an administrative access token was leaked over an insecure voice channel, and that our audio upload endpoint is vulnerable to path traversal.

Your objectives are to analyze the leaked audio, rotate the compromised credential, and secure the upload handler.

**Step 1: Identify and Rotate the Leaked Credential**
1. You have been provided with an intercepted audio recording at `/app/intercepted_voice_auth.wav`. You must transcribe this audio to find the leaked administrative token. 
2. The current active configuration is in `/app/auth_config.env`. It contains a variable `ADMIN_TOKEN`.
3. Replace the leaked token in `/app/auth_config.env` with a newly generated secure 32-character hex string.
4. Ensure the file permissions of `/app/auth_config.env` are set to `600` to prevent unauthorized read access.

**Step 2: Secure the Upload Handler**
Our audio file upload handler, written in Bash (`/app/upload_processor.sh`), processes raw HTTP-like requests from standard input. It reads headers and then the body. 
Currently, it has multiple critical flaws:
- It uses the `X-Upload-Filename` header directly to save the file, allowing path traversal (e.g., `../../../etc/passwd`).
- It does not properly enforce authentication.
- Saved files are written with unsafe default permissions.

You must rewrite `/app/upload_processor.sh` using **only Bash** (and standard utilities) to meet the following specifications:
1. **Authentication:** Parse the `Authorization: Bearer <token>` header. Compare the token against the `ADMIN_TOKEN` sourced from `/app/auth_config.env`. If missing or invalid, output exactly `HTTP/1.1 401 Unauthorized` and exit with code 1.
2. **Path Traversal Prevention:** Extract the filename from the `X-Upload-Filename` header. Strip any directory traversal components (i.e., extract only the basename). If the resulting basename is empty, output `HTTP/1.1 400 Bad Request` and exit with code 1.
3. **Extension Whitelisting:** Ensure the basename ends strictly with `.wav`. If not, output `HTTP/1.1 403 Forbidden` and exit with code 1.
4. **Secure Storage:** Save the request body (the file content) to `/app/safe_uploads/<basename>`. 
5. **File Permissions:** Ensure the newly created audio file in `/app/safe_uploads/` has permissions set to `600`.
6. On success, output exactly `HTTP/1.1 200 OK` and exit with code 0.

*Note: You may use standard CLI tools (like `grep`, `sed`, `awk`, `basename`, etc.) inside your Bash script. The incoming input will have standard Windows-style (`\r\n`) or Unix-style (`\n`) line endings for headers, followed by a blank line, followed by the body.*

**Step 3: Verification**
An automated verifier will evaluate your `/app/upload_processor.sh` script against a large suite of malicious and benign HTTP payloads to compute a security pass rate metric. You must achieve a 100% success rate to pass.