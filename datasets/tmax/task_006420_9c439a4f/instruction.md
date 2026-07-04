You are a security engineer tasked with rotating credentials for a legacy internal application. The application relies on a base64-encoded JSON cookie for session management and authentication. 

We have captured an HTTP request header dump from the application in `/home/user/headers.log`. 

Your task is to write and execute a Python script that does the following:
1. Parse `/home/user/headers.log` and extract the value of the `auth_session` cookie.
2. Base64-decode the cookie value and parse it as JSON.
3. You will notice a malicious Cross-Site Scripting (XSS) payload injected into the `profile_pic` field of the session object. Sanitize this by changing the `profile_pic` value to exactly `"default.png"`.
4. Rotate the credential for the user by updating the `token_hash` field. Replace the old hash with the SHA-256 hash of the new plaintext password: `NewSecurePassword123!`
5. Serialize the updated JSON object. Ensure there are no spaces between keys and values (e.g., use `separators=(',', ':')` in Python's `json.dumps`).
6. Base64-encode the new JSON string.
7. Write the updated HTTP cookie header line (e.g., `Cookie: auth_session=<new_base64_string>`) to a new file located at `/home/user/rotated_cookie.log`. Ensure the file contains only this single line with no trailing newlines.

Do not use external libraries outside of the Python standard library.