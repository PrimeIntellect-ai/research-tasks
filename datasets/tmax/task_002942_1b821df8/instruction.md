You are a forensics analyst recovering evidence from a compromised Linux host. The attacker exfiltrated a secret key, used it to encrypt a session token, and leveraged a privilege escalation vulnerability to take control of the system. We have recovered a bizarre video artifact left by the attacker and the encrypted token.

Your mission involves three phases:

### Phase 1: Video Artifact Analysis (Cryptanalysis)
The attacker encoded a 10-byte secret key into a video file located at `/app/evidence.mp4`.
- The video is exactly 8 seconds long at 10 frames per second (80 frames total).
- Each frame is completely solid black or solid white.
- A black frame represents a `0` bit, and a white frame represents a `1` bit.
- Parse the video frames sequentially. Every 8 frames represents one byte of the key, Most Significant Bit (MSB) first.
- Recover the 10-byte key and represent it as a 20-character lowercase hexadecimal string.

### Phase 2: Decryption and LPE Auditing
The attacker encrypted a token using a simple repeating-key XOR cipher. 
- The ciphertext is located at `/home/user/encrypted_token.bin`.
- Decrypt this file using the 10-byte key you recovered (XOR the first byte of the file with the first byte of the key, the second with the second, etc., wrapping the key every 10 bytes).
- The decrypted token will contain a string in the format: `VULNERABLE_TARGET=script_name.sh`.
- Look inside the directory `/home/user/scripts/`. You will find several Bash scripts. Audit the specific script named in the decrypted token.
- Identify the exact CWE (Common Weakness Enumeration) identifier that corresponds to the local privilege escalation vulnerability present in that script. The vulnerability will strictly be one of: CWE-78 (OS Command Injection), CWE-732 (Incorrect Permission Assignment), or CWE-377 (Insecure Temporary File).

### Phase 3: Reporting Service
You must bring up an HTTP reporting service so our automated collection system can retrieve your findings.
- Start an HTTP web server listening on `127.0.0.1:9090`.
- The server must respond to `GET /report` requests.
- The response MUST be a `200 OK` with a JSON body in the exact following format:
  ```json
  {
    "key": "<20-character hex string from Phase 1>",
    "script": "<the script name found in the decrypted token>",
    "cwe": "<the identified CWE string, e.g., CWE-78>"
  }
  ```
- Keep the server running in the background so the verifier can access it.

Ensure your server is up, bound to the correct port, and returns the strictly formatted JSON response before you finish.