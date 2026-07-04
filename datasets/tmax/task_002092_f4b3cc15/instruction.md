You are a forensics analyst responding to a compromised Linux host. The attacker left behind an encrypted evidence file (`/app/evidence.enc`) and a screen recording of their session (`/app/security_cam.mp4`).

Your objective is to recover the evidence and expose it securely for our automated incident response system.

**Phase 1: Video Analysis & Key Recovery**
The attacker's screen recording (`/app/security_cam.mp4`) contains a hidden visual watermark. The attacker used a custom tool that flashed a pure red block (RGB: 255, 0, 0) in the top-left corner (from pixel x=0,y=0 to x=9,y=9) on certain frames. 
1. You must analyze the video and count the exact number of frames that contain this red block.
2. Let this frame count be `C`. The decryption passphrase for the evidence is the string `"PIN:"` followed immediately by `C` (for example, if there are 50 frames, the passphrase is `PIN:50`).

**Phase 2: Decryption**
The file `/app/evidence.enc` is encrypted using AES-256-CBC.
1. The 32-byte encryption key is the SHA-256 hash of the passphrase (encoded in UTF-8).
2. The first 16 bytes of `/app/evidence.enc` are the plaintext Initialization Vector (IV).
3. The rest of the file is the ciphertext. 
4. Decrypt the file. The recovered plaintext is a JSON document containing two keys: `"auth_token"` and `"recovered_data"`.

**Phase 3: Secure API Exposure**
Our incident response systems need to pull this data programmatically. 
1. Write and start a Python-based HTTP server listening on `0.0.0.0:8000`.
2. The server must expose a single endpoint: `GET /api/v1/evidence`.
3. The endpoint must require HTTP Bearer Authentication using the exact `"auth_token"` value extracted from the decrypted JSON. If the token is missing or incorrect, return a `401 Unauthorized`.
4. On successful authentication, return an HTTP 200 OK with the contents of the `"recovered_data"` object as a JSON payload.

Run the server in the background or leave it running in your terminal so our verification system can connect to it. Make sure your server doesn't crash on invalid inputs.