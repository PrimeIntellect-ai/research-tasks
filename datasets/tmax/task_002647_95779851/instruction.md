We intercepted a surveillance video file located at `/app/intercept.mp4`. We believe the video contains a brief flash of a QR code that holds instructions for our evasion payload delivery system. 

The QR code contains two lines of text:
1. `HASH:<sha256_hash>` - The SHA-256 hash of a 4-digit numerical PIN.
2. `DATA:<base64_string>` - A payload encrypted with OpenSSL `aes-256-cbc` (using `-pbkdf2` and `-salt`). The passphrase used to encrypt this data is the 4-digit PIN itself.

Your objective is to extract the payload and host it securely:
1. Extract the frames from `/app/intercept.mp4` and decode the QR code. You may use `ffmpeg` and `zbarimg` (or any other tool of your choice).
2. Brute-force or crack the 4-digit PIN using the provided SHA-256 hash.
3. Decrypt the `DATA` string using OpenSSL, providing the cracked PIN as the password.
4. The decrypted plaintext will be in the format `PORT=...;TOKEN=...;PAYLOAD=...`. Parse these values.
5. Write and start a simple HTTP web server (in Python, Ruby, or any language you prefer) listening on `0.0.0.0` at the specified `PORT`.
6. The server must expose a `GET /download` endpoint.
7. The endpoint must check for an HTTP header named `X-Auth`. 
8. If the `X-Auth` header exactly matches the extracted `TOKEN`, return an HTTP 200 OK with the `PAYLOAD` string as the plain text response body. If the header is missing or incorrect, return an HTTP 403 Forbidden.

Leave your HTTP server running so it can be automatically tested by our verification suite.