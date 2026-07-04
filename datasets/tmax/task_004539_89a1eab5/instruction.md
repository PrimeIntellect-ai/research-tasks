You are acting as a network security engineer investigating a recent compromise. We have recovered a video recording of an administrator's terminal session, located at `/app/admin_session.mp4`. The administrator was interacting with a legacy login portal that we suspect is vulnerable to an open redirect and potentially XSS.

Your objective is to complete the following multi-stage workflow:

1. **Video Analysis**: Analyze the video `/app/admin_session.mp4` using `ffmpeg` and any Python script you need. Extract the hidden administrative base64-encoded session token that flashes on screen between frames 150 and 160. Save this token exactly as it appears into `/home/user/extracted_token.txt`.

2. **TLS Certificate Generation**: Generate a self-signed RSA TLS certificate and private key in `/home/user/certs/` named `server.crt` and `server.key`.

3. **Malicious HTTPS Server**: Write and run a Python HTTPS server (using the generated certificates) that listens on `127.0.0.1:8443`. This server will act as the destination for our open redirect exploit.
   - When the server receives an HTTPS GET request to `/callback`, it must inspect the `Cookie` header.
   - It must validate that the `session_id` cookie matches the token you extracted from the video.
   - If it matches, the server must respond with an HTTP 200 OK and a body containing the string: `EXFILTRATION_SUCCESS`.
   - If it does not match, or the cookie is missing, respond with an HTTP 403 Forbidden.

4. **Exploit Payload**: Craft an open redirect payload URL targeting `https://victim-portal.local/login?redirect=...` that would redirect an authenticated user to your malicious server's `/callback` endpoint. Write this full malicious URL into `/home/user/payload.txt`.

Ensure your server remains running in the background so our automated verification systems can test the endpoint. Do not use any external third-party libraries for the web server; use Python's built-in `http.server` and `ssl` modules.