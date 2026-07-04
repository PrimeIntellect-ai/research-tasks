You are a penetration tester investigating a suspected breach on an internal network. We have intercepted a strange video file broadcasted by the malware, located at `/app/exfiltration_feed.mp4`. Our initial analysis suggests the attacker is using this video feed to stealthily distribute C2 (Command and Control) instructions, authentication cookies, and certificate chains to compromised nodes via steganography-like frame flashing.

Your task is to analyze this video, recover the C2 server configuration, and stand up a mock C2 service (a honeypot) to intercept the attacker's incoming callbacks.

Perform the following steps:

1. **Video Data Extraction:** Use `ffmpeg` to extract the frames from `/app/exfiltration_feed.mp4`. The video contains periodic frames (exactly every 30th frame, i.e., frame 0, 30, 60...) that display a plain text string in the center of the frame. 
2. **Reverse Engineering & Assembly:** Extract the text from these specific frames (using OCR tools like `tesseract` which are available on the system, or by writing a Python script using OpenCV/Pillow and pytesseract). Concatenate these strings in order. The resulting string is a base64-encoded JSON object.
3. **Configuration & Integrity Verification:** Decode the JSON object. It will contain three keys:
   - `cert_b64`: A base64-encoded PEM certificate.
   - `expected_cookie`: A specific session cookie string the attacker uses for authentication.
   - `sha256_checksum`: The SHA256 hash of the decoded certificate.
   Verify that the SHA256 checksum matches the decoded certificate. If it does not, you must log "INTEGRITY_FAILURE" to `/home/user/verification.log` and halt.
4. **Honeypot Deployment:** Write and run a Python server (using only standard libraries like `http.server` and `ssl`) that acts as the C2 honeypot. 
   - The server must listen on **TCP port 8443** (HTTPS) and **TCP port 8080** (HTTP) on `127.0.0.1`.
   - You must use the recovered `cert_b64` to secure the HTTPS listener (save it as `/home/user/server.pem` and generate a dummy private key for it if necessary to bind, or just terminate TLS).
   - The HTTP and HTTPS listeners must inspect incoming `GET` requests to the `/callback` endpoint.
   - If the request contains the `Cookie` header exactly matching the `expected_cookie` recovered from the video, the server must respond with HTTP 200 OK and the plaintext body: `ACK_AUTH_VALID`.
   - If the cookie is missing or incorrect, it must respond with HTTP 403 Forbidden and the body: `ERR_UNAUTHORIZED`.
   - For all valid requests, append the request's `User-Agent` header to `/home/user/access.log`.

Keep the server running so our automated verifier can probe it using different protocols and headers.