You are a security engineer tasked with rotating credentials after a vulnerability assessment revealed an open redirect vulnerability in a legacy authentication service. 

An attacker exploited an endpoint (`/login`) to redirect users to malicious domains, causing their authentication tokens to be leaked in the referrer headers or URLs.

You need to analyze the server logs, identify the compromised users, and write a Rust program to rotate their tokens, secure the updated configuration, and verify its integrity.

The server files are located in `/home/user/server/`. (Assume these files exist):
1. `/home/user/server/access.log`: The web server access logs.
2. `/home/user/server/users.json`: A JSON array of user objects containing current credentials. Format: `[{"username": "...", "token": "..."}, ...]`

**Your Tasks:**
1. **Intrusion Detection (Pattern Matching):**
   Analyze the `/home/user/server/access.log` file. An entry indicates a leaked token if a `GET /login` request contains a `redirect` query parameter pointing to a domain *other than* `http://internal.corp` or `http://localhost`, and it contains a `token` query parameter. 
   
2. **Token Rotation (Rust Program):**
   Create a new Rust project in `/home/user/rotator`. Write and run a Rust program that reads `users.json` and the `access.log`.
   For every user whose token was identified as leaked in step 1, generate a new token. 
   *Note: To allow for automated verification of this task, the new token MUST be the SHA-256 hash of the string `ROTATED_<username>` (e.g., if the user is `admin`, the new token is the hex-encoded SHA-256 hash of `ROTATED_admin`).*
   Users whose tokens were not leaked should keep their original tokens.

3. **Output Configuration:**
   Your Rust program should write the updated user list to `/home/user/server/users_rotated.json`.
   To ensure consistent file integrity verification, the output JSON must be a compact, minified JSON array (no spaces, no newlines), and the user objects inside the array must be sorted alphabetically by their `username`. The keys inside the objects must also be ordered alphabetically (i.e., `{"token":"...","username":"..."}`).

4. **File Permissions:**
   The new configuration file contains sensitive tokens. Set the file permissions of `/home/user/server/users_rotated.json` to `0600` so that only the owner has read and write access.

5. **File Integrity Verification:**
   Compute the SHA-256 hash of the final `/home/user/server/users_rotated.json` file. Save just the hex-encoded hash string (with no trailing newline or filename) to a new file at `/home/user/server/users_rotated.json.sha256`.

Complete all steps using the terminal. You may use shell commands alongside your Rust program.