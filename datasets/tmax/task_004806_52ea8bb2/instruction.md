You are a compliance analyst tasked with generating and securely serving an SSH audit trail. Your goal is to recover a legacy administrator passphrase, audit an SSH configuration file, and stand up a secure logging service.

**Step 1: Credential Recovery**
An image of an old sticky note containing the root of the administrator's passphrase is located at `/app/sticky_note.png`. 
1. Extract the text from this image. It contains a base word.
2. The actual passphrase is the extracted base word followed by a single digit (0-9). 
3. Use this passphrase to decrypt the SSH private key located at `/app/admin_key.enc`. Output the decrypted SSH key to `/home/user/admin_key.pem`.

**Step 2: SSH Configuration Audit**
You have been provided with an SSH configuration file at `/app/sshd_config.target`. 
Analyze this file and create an audit report at `/home/user/ssh_audit.json`. The JSON must contain a single dictionary mapping the names of insecure directives found in the file to their *compliant* secure values. 
Specifically, check for and report the secure overrides for: `PermitRootLogin` (should be no), `PasswordAuthentication` (should be no), and `X11Forwarding` (should be no). Only include the ones that are currently insecure in the target file.

**Step 3: Secure Audit Logging Service**
Create and start a web service listening on `127.0.0.1:8080`. You may use any programming language.
The service must implement the following:
1. **POST `/log`**: Accepts an `application/x-www-form-urlencoded` request with a field named `entry`. 
   - *Security Requirement*: To prevent XSS in our audit viewers, any HTML characters (`<`, `>`, `&`, `"`, `'`) in the `entry` payload MUST be strictly HTML-entity encoded before being saved.
   - The sanitized entry should be appended to `/home/user/service_audit.log` on a new line.
   - Return an HTTP 200 OK.
2. **GET `/report`**: Returns the contents of `/home/user/ssh_audit.json`.
   - *Authentication Requirement*: This endpoint must be protected. It should require an `Authorization: Bearer <passphrase>` header, where `<passphrase>` is the exact multi-character passphrase you cracked in Step 1. Return 401 Unauthorized if the token is missing or invalid.

Leave the service running in the background when you are finished. Ensure all files are correctly placed and the service is actively listening on port 8080.