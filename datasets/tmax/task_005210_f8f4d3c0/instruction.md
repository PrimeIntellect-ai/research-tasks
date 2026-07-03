You are a compliance analyst tasked with replacing a legacy, vulnerable audit-log upload server. The previous C-based server (`/app/legacy_auditor`) was susceptible to path traversal and has been decommissioned. You need to implement a secure replacement using a Bash CGI script.

**Part 1: Authentication Recovery**
The credentials for the audit service were lost, but we have two clues:
1. An audio note left by the previous admin at `/app/admin_note.wav`. You must transcribe this audio to recover the base passphrase.
2. The decommissioned ELF binary `/app/legacy_auditor`. Analyze this binary to find:
   - The custom HTTP header used for authentication.
   - The cryptographic salt.

The SHA-256 hash of the final authentication token is stored in `/app/token_hash.txt`. 
The actual token is constructed as: `<transcribed_passphrase><salt><2-digit-number>`.
Use password cracking/brute-force techniques to discover the exact 2-digit number (00-99) and recover the full authentication token.

**Part 2: Secure Implementation**
Create a Bash CGI script at `/app/cgi-bin/upload.sh` to handle file uploads securely.
Your script must:
1. Reject any request that does not include the correct custom HTTP header and recovered token. Return a `401 Unauthorized` HTTP status.
2. Accept HTTP POST requests containing raw file data in the body.
3. Read the intended filename from the `HTTP_X_FILENAME` environment variable.
4. **Prevent Path Traversal:** Securely sanitize the filename so that the file is strictly saved into `/app/audit_logs/`. Any attempt to use `../` or absolute paths pointing outside this directory must be rejected with a `400 Bad Request` status.
5. **Integrity Verification:** Read the expected SHA-256 hash from the `HTTP_X_FILE_HASH` environment variable. After saving the file, verify its integrity. If the hash does not match the uploaded content, delete the file and return a `422 Unprocessable Entity` status.
6. If all checks pass, return a `200 OK` status with the word `SUCCESS`.

**Part 3: Deployment**
1. Ensure `/app/audit_logs/` exists and is writable.
2. Ensure `/app/cgi-bin/upload.sh` is executable.
3. Start a CGI-enabled web server on port `8080` bound to `0.0.0.0` with its root directory set to `/app`. (You may use `python3 -m http.server 8080 --cgi` from the `/app` directory). Leave the server running in the background.

Ensure your Bash script properly handles standard CGI input/output, including printing the `Content-Type: text/plain` header followed by an empty line before the body.