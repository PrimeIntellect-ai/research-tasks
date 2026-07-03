You are a network engineer tasked with analyzing and replacing a legacy authentication daemon. We have lost the source code to our custom authentication service, leaving us with only a stripped, compiled binary located at `/app/auth_service`. 

We need you to reverse-engineer this binary to understand its cryptographic checksum mechanism, and then write a replacement service that is more secure. 

Your new service must be written in Python (or another language of your choice) and must run in the background, listening for raw TCP connections on `127.0.0.1:8080`.

### Protocol Specification
Incoming requests are single lines of text terminated by a newline character (`\n`).
Format: `AUTH v1 <USERNAME> <CHECKSUM> <PAYLOAD>`
- `<USERNAME>`: The user's name.
- `<CHECKSUM>`: A 32-character lowercase MD5 hash.
- `<PAYLOAD>`: A hex-encoded string containing the user's data.

### Validation Rules (Must be evaluated in this exact order)
1. **Intrusion Detection (NEW RULE)**: 
   The original binary was vulnerable to injection attacks. In your new service, you must first inspect the `<USERNAME>` field. If the username contains any of the following restricted characters: `'`, `"`, `;`, `<`, or `>`, you must immediately respond with `REJECT: INTRUSION\n` and close the connection.

2. **Integrity Verification**: 
   The original binary computes an MD5 hash to verify the payload's integrity. It concatenates the *exact hex string* provided in the `<PAYLOAD>` field with a hardcoded secret salt, and takes the MD5 hash of the resulting string. 
   You must reverse-engineer the `/app/auth_service` binary to extract this secret salt. 
   If the provided `<CHECKSUM>` does not match your computed MD5 hash, respond with `REJECT: INTEGRITY\n` and close the connection.

3. **Authentication Flow**:
   If the request passes the intrusion and integrity checks, decode the hex `<PAYLOAD>`. 
   - If the decoded payload contains the exact substring `admin`, respond with `ACCEPT: ADMIN\n` and close the connection.
   - Otherwise, respond with `ACCEPT: USER\n` and close the connection.

### Execution
Create your service script at `/home/user/new_auth_service.py` (or another appropriate extension). Start the service so that it binds to `127.0.0.1:8080` and continues to handle multiple sequential connections in the background. Do not stop the service once started; it will be tested by an automated verification suite.