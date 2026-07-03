You are a network security engineer investigating a recent compromise. We have a screen recording (`/app/capture.mp4`) of a victim's browser session. During the session, the victim logs into our portal, but an open redirect vulnerability forces their browser to send their session token to an attacker's domain.

Your task is to:
1. Extract the frames from `/app/capture.mp4` using `ffmpeg` and perform OCR (using `tesseract`) to recover the leaked authentication token from the browser's address bar.
2. Analyze the server security logs in `/app/auth_logs.json` to find the session details corresponding to the leaked token's timestamp and user ID.
3. The logs contain a debugging error that accidentally leaked the HMAC secret used for token signing during that specific hour. Extract this secret.
4. Using the secret and the token format (JWT-like, base64-encoded header.payload.signature), write a Bash script at `/home/user/forge.sh` that generates a new, valid token for the user `admin` with an expiration time set to `timestamp + 3600`.
5. Your script `/home/user/forge.sh` must accept a timestamp as its first argument and output ONLY the forged token to stdout.

The automated verification system will run your script 50 times with different timestamps and test the generated tokens against our authentication validation tool. You must achieve an accuracy of at least 95% valid tokens.