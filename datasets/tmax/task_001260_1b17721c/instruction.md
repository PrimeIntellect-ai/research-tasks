You are an incident responder analyzing a compromised Linux host. The attacker left behind several traces, and we need you to piece them together to recover the original authentication logs they attempted to obfuscate.

Here is the evidence available to you:
1. **`/app/auth.log`**: A standard Linux authentication log file. The attacker performed a brute-force attack from a specific IP address (many failed passwords followed by an "Accepted password" for the user `admin`).
2. **`/app/evidence.png`**: A screenshot the attacker accidentally dropped. You must extract the text from this image to find the attacker's master encryption key (labeled `MASTER_KEY=...`).
3. **`/app/manifest.sha256`**: A list of known-good SHA256 hashes for the system binaries located in `/app/bin/`. One of the binaries in `/app/bin/` has been tampered with and its hash will not match the manifest.
4. **`/app/obfuscated_records.txt`**: A large dataset of obfuscated logs the attacker tried to hide.

Your task:
1. Identify the compromised IP address from `/app/auth.log`.
2. Extract the master key from `/app/evidence.png` using OCR (e.g., `tesseract`).
3. Identify the tampered binary in `/app/bin/`.
4. Write a Python script at `/home/user/recover.py` that processes `/app/obfuscated_records.txt`. 

The obfuscation method used by the attacker on `obfuscated_records.txt` is as follows:
- Each line is a base64 encoded string.
- When decoded, it results in a JSON string containing `{"ip": "...", "timestamp": "...", "event": "...", "signature": "..."}`.
- To verify the integrity of the record, compute the HMAC-SHA256 of the concatenated string `<ip>|<timestamp>|<event>` using the `MASTER_KEY` extracted from the image. 
- If the first 10 characters of the computed HMAC hex digest match the `signature` field, the record is valid.
- Additionally, you must tag the record as `compromised: true` if the IP matches the attacker's IP found in `auth.log`, and `compromised: false` otherwise.

Your script `/home/user/recover.py` must output a JSON array of only the valid records to `/home/user/recovered_logs.json`. Each object in the array should look exactly like:
`{"ip": "...", "timestamp": "...", "event": "...", "compromised": true/false}`

The accuracy of your recovered JSON file will be evaluated against our hidden ground truth. You must achieve an accuracy of at least 95%.