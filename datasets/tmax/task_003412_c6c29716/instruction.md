You are a web developer building a secure "Video Signature Verification API" using Bash. Your team has decided to implement a fast, stateless authentication microservice that reads encoded challenges directly from a security video feed and evaluates them.

You must build and run an HTTP server in Bash (using tools like `socat` or `nc`) that listens on `127.0.0.1:8080`. 

**API Specification:**
- **Endpoint:** `GET /api/v1/video-auth?ts=<timestamp>`
- **Behavior:**
  1. Parse the `ts` parameter (which represents a time in seconds, e.g., `1`, `2.5`).
  2. Use `ffmpeg` to extract a single video frame at the exact `<timestamp>` from the video file located at `/app/auth_events.mp4`.
  3. Use `zbarimg` to decode a QR code present in that specific frame.
  4. The decoded QR code contains a simple mathematical expression (e.g., `10 + 5`, `22 * 3`). You must parse and evaluate this expression.
  5. Encode the evaluated integer result in Base64.
  6. Return an HTTP 200 response with the Base64 string as the body.
  
**Response Format (Success):**
```http
HTTP/1.1 200 OK
Content-Type: text/plain

<base64_encoded_result>
```

**Web Security Constraints:**
This endpoint will be subjected to adversarial testing. 
1. The `ts` parameter may contain shell injection attempts (e.g., `1; rm -rf /`).
2. The decoded QR codes from the video may contain malicious payloads instead of valid mathematical expressions (e.g., `system("wget ...")`, `$(cat /etc/passwd)`). 
If the `ts` parameter is malformed, or if the QR code payload contains anything other than numbers, spaces, and basic math operators (`+`, `-`, `*`, `/`), your server must block the request and return:
```http
HTTP/1.1 400 Bad Request
Content-Type: text/plain

Invalid Input
```

**Instructions:**
1. Create your server script at `/home/user/server.sh`.
2. Make sure it uses a tool like `socat TCP-LISTEN:8080,reuseaddr,fork EXEC:/home/user/handler.sh` to handle concurrent requests.
3. Start your server in the background so it is actively listening on port `8080` when you consider the task complete.
4. You may write a test script (`/home/user/test.sh`) to verify your service orchestration and encoding logic locally.