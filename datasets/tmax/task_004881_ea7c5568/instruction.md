You are an incident responder investigating a compromised Linux server. We suspect an attacker left behind an encrypted payload, a rogue background process, and an intercepted audio message. Your task is to analyze these artifacts, decrypt the evidence, and stand up a secure containment service to intercept the attacker's callbacks.

Here are the steps you must complete:

1. **Audio Analysis:** 
   Analyze the intercepted voicemail located at `/app/voicemail.wav`. The attacker states the passphrase used to encrypt their payloads. You may need to install transcription tools (e.g., `ffmpeg`, `openai-whisper` via pip) to extract the passphrase from the audio.

2. **Process Auditing & Credential Extraction:**
   The attacker executed a rogue script that is currently running on the system. Investigate the system's running processes (e.g., by analyzing `/proc` or using `ps`) to find a process running `/home/user/rogue_worker.py`. This script was launched with command-line arguments that leak a cryptographic salt (`--salt <HEX_SALT>`). Extract this salt.

3. **Decryption & Hashing:**
   You have an encrypted evidence file at `/home/user/evidence.enc`. 
   Using Python, write a script to decrypt this file. The file was encrypted using AES-256-CBC. The key must be derived using PBKDF2HMAC (SHA256, 100,000 iterations) with the passphrase extracted from the audio and the salt extracted from the rogue process. The IV is prepended to the ciphertext (the first 16 bytes of the file).
   The decrypted file will be a JSON string containing an `auth_token` and a `listen_port`. Save the decrypted JSON to `/home/user/decrypted_evidence.json`.

4. **Secure Service Setup:**
   The attacker's malware will attempt to send data to a local endpoint. You must stand up a Python-based HTTP server (e.g., using Flask, FastAPI, or `http.server`) listening on `127.0.0.1` at the `listen_port` specified in the decrypted JSON.
   
   The server MUST meet these requirements:
   - Listen on `127.0.0.1:<listen_port>`.
   - Implement a `POST` endpoint at `/callback`.
   - Require an `Authorization: Bearer <auth_token>` header, using the exact token from the decrypted JSON. If the token is missing or invalid, return an HTTP 401 status code.
   - Read the incoming POST request body (raw bytes) and compute its SHA-256 hash.
   - Return an HTTP 200 JSON response in this exact format: `{"status": "received", "sha256": "<computed_hex_digest>"}`.
   
Keep your server running in the background or in a separate terminal session so it can be verified by the testing suite.