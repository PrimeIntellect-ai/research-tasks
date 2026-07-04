You are an expert security auditor. We have intercepted an application deployment that handles sensitive audio transcriptions, but it contains critical security flaws. You must extract a secret credential, audit and patch the application, and deploy the secure version.

**Step 1: Audio Signal Analysis**
We captured a suspicious audio transmission saved at `/app/intercepted_signal.wav`. 
It contains an audio transmission of Morse code. Decode the Morse code to reveal a secret authentication token. Write this decoded token (in uppercase) to `/home/user/token.txt`.

**Step 2: Vulnerability Analysis & Secure Coding**
There is a Flask application located at `/home/user/server.py`. It is currently configured to receive uploaded audio files on the `/upload` endpoint via POST requests, but it is deeply flawed:
1.  **Authentication:** It currently lacks any authentication.
2.  **Path Traversal:** The file upload handler blindly trusts the `filename` provided in the form data, making it vulnerable to path traversal (e.g., an attacker could overwrite `/home/user/.ssh/authorized_keys`).
3.  **File Permissions:** It saves uploaded files with insecure default permissions.

Modify `/home/user/server.py` to implement the following security requirements:
*   **Authentication:** The `/upload` endpoint MUST require an `X-Auth-Token` HTTP header. The value must exactly match the secret token you extracted in Step 1. If the header is missing or incorrect, return a `401 Unauthorized` status code.
*   **Path Traversal Protection:** Sanitize the uploaded filename so that directory traversal is impossible. You should extract only the base filename (ignoring any path prefixes like `../` or `/`). Save the file securely inside `/home/user/uploads/`.
*   **Access Control:** Immediately after saving the file, explicitly set the uploaded file's permissions to `0600` (read and write for the owner only) to prevent unauthorized local access.

**Step 3: Service Deployment**
Ensure the directory `/home/user/uploads/` exists.
Run your patched Flask application so that it listens on `127.0.0.1:8000`. Leave the server running in the background.

An automated verifier will issue real HTTP requests to your running service on port 8000 to verify that authentication is enforced, path traversal is mitigated, and file permissions are properly restricted.