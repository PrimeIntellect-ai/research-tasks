You are a security engineer tasked with rotating credentials and fixing a vulnerability in a legacy authentication microservice written in C.

A previous developer left behind a rudimentary HTTP authentication service located at `/home/user/auth_service/auth.c`. The service listens on port 8080 and handles login redirects. 

Currently, the service has two major issues:
1. **Hardcoded Credential Dependency:** It only reads from `/home/user/auth_service/old_secret.key`. We are in the process of rotating to a new secret located at `/home/user/auth_service/new_secret.key`.
2. **Open Redirect Vulnerability:** The service blindly uses the `redirect` query parameter in the HTTP `Location` header upon successful authentication.

Your task is to fix the code and verify the fixes:

**Step 1: Code Modifications (`/home/user/auth_service/auth.c`)**
- **Credential Rotation:** Modify the token validation logic so that it accepts tokens signed with *either* the old secret OR the new secret. The service extracts a Base64 encoded token from the `Authorization: Bearer <token>` header, decodes it, and compares it to the secret.
- **Open Redirect Fix:** Analyze the redirect extraction logic. Modify the code so that if the `redirect` parameter starts with `http://` or `https://` (indicating an external domain), it defaults to `/dashboard`. Only relative paths (e.g., `/settings`, `/profile`) should be allowed in the `Location` header.

**Step 2: Compilation and Execution**
- Compile your modified code to `/home/user/auth_service/auth_server`.
- Start the server in the background.

**Step 3: Verification Log**
Create a verification log at `/home/user/auth_service/verification.log` by making three specific `curl` requests to your running server (`http://127.0.0.1:8080/login?redirect=...`). 
For each request, append a single line to the log file in this exact format:
`TEST_NAME: HTTP_STATUS | LOCATION_HEADER_VALUE` (If no Location header is present, write `NONE`).

The three tests you must log are:
1. `OLD_TOKEN_VALID`: Use a valid Base64 encoded token matching `old_secret.key` and `redirect=/home`.
2. `NEW_TOKEN_VALID`: Use a valid Base64 encoded token matching `new_secret.key` and `redirect=/settings`.
3. `OPEN_REDIRECT_BLOCKED`: Use a valid Base64 encoded token matching `new_secret.key` and `redirect=https://evil.com/login`.

Do not use any external C libraries beyond the standard library (`libc`). A Base64 decoding function is already provided in the starter code.