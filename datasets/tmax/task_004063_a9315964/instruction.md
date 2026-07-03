You are an incident responder investigating a compromised server. The attacker left behind a video file at `/app/evidence.mp4`. Analysts believe this video acts as a covert communication channel containing the key to the attacker's command and control backdoor.

Your task is to reverse-engineer the secret key from the video and establish a honeypot service in Go to intercept further attacker payloads.

Step 1: Video Analysis & Cryptographic Key Derivation
1. Use `ffmpeg` (preinstalled) and standard shell tools to extract and analyze the frames of `/app/evidence.mp4`.
2. Count the exact number of frames in the video that are completely pure red (every pixel is exactly RGB: 255, 0, 0).
3. Compute the SHA-256 hash of the string `RED_FRAMES_<COUNT>`, where `<COUNT>` is the exact integer number of pure red frames you found. (Do not include a trailing newline in the hashed string). This hex-encoded hash is the `SECRET_KEY`.

Step 2: Service Deployment
Write and start a Go web server listening on `127.0.0.1:8080`. The server must implement the following endpoints to act as the honeypot:
1. `GET /health`
   - Must return HTTP status 200 OK with the exact body `OK`.
2. `POST /command`
   - Must check for the HTTP header `X-Secret-Key`.
   - If the header value exactly matches your derived `SECRET_KEY`, return HTTP status 200 OK with the exact body `COMMAND_ACCEPTED`.
   - If the header is missing or incorrect, return HTTP status 401 Unauthorized.

Run your Go server in the background so it remains active. Our automated verification system will send real HTTP requests to your service to test if the key was derived correctly and the honeypot is properly implemented.