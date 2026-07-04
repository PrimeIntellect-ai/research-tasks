You are acting as an incident response engineer. We recently suffered a breach. The attacker left a gloating audio log detailing exactly how they bypassed our system and leaked our credentials. 

Your objectives are to:

1. **Analyze the Audio Artifact:**
   An audio file is located at `/app/incident_log.wav`. You must transcribe this audio file (you may install tools like `openai-whisper` via pip, or any other transcription method available in the environment) to discover:
   - The specific port number the attacker targeted.
   - The specific secret key that was compromised.
   - The vulnerability technique they used.

2. **Audit and Redact:**
   - Scan the system to find the service running on the port mentioned in the audio. The source code for this service will be located in `/home/user/service/`.
   - The attacker mentioned a compromised secret. You must search through all `.log` files in `/home/user/logs/` and redact this sensitive data. Replace every instance of the exact compromised secret string with the literal string `[REDACTED]`.

3. **Implement a Secure JWT Validator:**
   The vulnerability was related to a JWT implementation that accepts tokens with `algorithm=none` or fails to verify signatures properly. 
   You must write a completely secure, standalone JWT validator script in Python at `/home/user/jwt_validator.py`.
   
   **Requirements for `/home/user/jwt_validator.py`**:
   - Must be executable as `python3 /home/user/jwt_validator.py --secret <SECRET_KEY>`
   - It must read a single JWT string from `stdin`.
   - It must strictly validate the signature using `HS256` and the provided secret.
   - It MUST reject any token where the algorithm is `none` (case-insensitive) or any algorithm other than `HS256`.
   - It must output strictly valid JSON to `stdout` and exit with code 0.
   - If the token is perfectly valid and the signature matches, output: `{"status": "valid", "payload": <decoded_payload_dict>}`
   - If the token is invalid (bad signature, `alg=none`, malformed, wrong algorithm), output: `{"status": "invalid"}`
   - Do not output any other text or logging to `stdout`.

Ensure your `/home/user/jwt_validator.py` implementation is bit-exact in its JSON output logic compared to standard secure implementations. We will fuzz your script with thousands of forged, manipulated, and valid JWTs to ensure no bypass is possible.