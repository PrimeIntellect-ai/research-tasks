You are acting as a DevSecOps engineer tasked with enforcing a strict API security policy using only Bash and standard command-line tools. We need a lightweight API gateway that inspects incoming JSON Web Tokens (JWT) to mitigate the "algorithm=none" vulnerability before requests reach our internal service.

Your task has three parts:

1. **Information Extraction (Audio):**
   Listen to the audio file located at `/app/voicemail.wav` using available transcription tools (like `whisper` or by downloading it). The audio contains a dictated 4-character alphanumeric Policy ID (e.g., if it dictates "alpha bravo one two", the ID is `AB12`).

2. **Policy Handler Script:**
   Write a Bash script at `/home/user/handler.sh` that processes raw HTTP/1.1 GET requests from standard input.
   - It must extract the JWT from the `Authorization: Bearer <token>` header.
   - It must decode the base64url-encoded JWT header.
   - If the JWT header specifies `"alg":"none"` (case-insensitive, e.g., `none`, `None`, `NONE`), the script must return exactly:
     `HTTP/1.1 403 Forbidden\r\n\r\nPolicy Violation\n`
   - If the JWT has any other algorithm, the script must return exactly:
     `HTTP/1.1 200 OK\r\nX-Policy-ID: <EXTRACTED_POLICY_ID>\r\n\r\nAccess Granted\n`
     (Replace `<EXTRACTED_POLICY_ID>` with the uppercase 4-character ID transcribed from the audio).
   - Make sure your script handles standard Base64url padding issues appropriately.

3. **Gateway Server:**
   Write a launcher script at `/home/user/start_gateway.sh` that uses `socat` to listen for TCP connections on `127.0.0.1:8080` and forks your `/home/user/handler.sh` for each incoming connection. The gateway must be running in the background when you complete the task.

Requirements:
- Only standard Linux utilities (bash, grep, awk, sed, base64, jq, socat, tr) may be used.
- Do not use Python, Node.js, or compiled languages for the web server or handler.
- Ensure the gateway is running on port 8080 before finishing.