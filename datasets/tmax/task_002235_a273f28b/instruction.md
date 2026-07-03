You are acting as a penetration tester analyzing a suspected insider threat. We have intercepted a screen recording of the attacker's terminal, located at `/app/surveillance_capture.mp4`. 

Your objectives are as follows:

1. **Video Analysis & Token Extraction:**
   The video contains a flashing text overlay between frames 120 and 150. Use `ffmpeg` and Python (e.g., OpenCV or standard image processing libraries, tesseract if needed) to extract this text. The text is a base64-encoded, AES-256-CBC encrypted session token.

2. **Decryption:**
   You will find a partially written script at `/home/user/decryptor.py` containing the AES key and IV used by the attacker. Fix the script, verify the file integrity of the extracted token, and decrypt the text to reveal the plaintext authentication token.

3. **Secure Reporting Service setup:**
   Write and run a Python HTTP web server listening exactly on `127.0.0.1:8080`. This service acts as a secure vulnerability reporting endpoint. 
   The server must handle incoming HTTP POST requests to the `/report` endpoint.
   
   **Authentication:** The server must strictly require an `Authorization: Bearer <plaintext_token>` header, where `<plaintext_token>` is the exact decrypted token from step 2. Return HTTP 401 Unauthorized if missing or incorrect.
   
   **Payload Processing:** The POST request body will be JSON in the format:
   `{"xss_payload": "<some_injected_script>", "victim_email": "user@domain.com"}`
   
   Your server must:
   a) Perform vulnerability analysis by identifying if the `xss_payload` contains standard HTML script tags.
   b) Perform sensitive data redaction: You must replace the `victim_email` completely with the exact string `[REDACTED]`.
   c) Calculate the SHA-256 hash of the exact `xss_payload` string to ensure payload integrity tracking.
   
   **Response:**
   The server must respond with HTTP 200 OK and a JSON body containing:
   `{"status": "analyzed", "redacted_email": "[REDACTED]", "payload_hash": "<computed_sha256_hash>"}`

Ensure the server stays running so the automated verifier can send multiple protocols/requests to it. Do not use external network services to solve this. Write all logs to `/home/user/server.log`.