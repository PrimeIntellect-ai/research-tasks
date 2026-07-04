You are a network engineer analyzing intercepted communications from a suspected malicious actor. You have recovered two key artifacts: an encrypted data payload captured from network traffic, and an intercepted audio transmission that we believe contains the decryption key. 

Your objective is to extract the key, decrypt the payload, secure your local environment, and expose the recovered intelligence via a secure multi-protocol service for our automated systems to ingest.

**Step 1: Audio Analysis & Decryption**
1. Analyze the audio file located at `/app/intercepted.wav`. It contains a spoken sequence of digits in English.
2. The transcribed sequence of digits forms a numeric PIN.
3. Read the encrypted hex-encoded payload located at `/home/user/traffic.enc`. 
4. Decrypt the payload. The encryption used is a repeating-key XOR cipher, where the key is the string representation of the transcribed PIN (e.g., if the PIN is "123", the key is "123").

**Step 2: Secure Key Management**
1. Create the `/home/user/.ssh` directory if it does not exist and enforce strict access control (only the owner should have read/write/execute permissions).
2. Generate an Ed25519 SSH keypair named `id_ed25519` inside `/home/user/.ssh/` with no passphrase.
3. Apply standard SSH hardening permissions to the generated keys (the private key must not be readable by anyone but the owner).

**Step 3: Multi-Protocol Intelligence Server**
Write a Python script named `/home/user/server.py` and run it in the background. The script must simultaneously serve two protocols:
1. **HTTP Service (Port 8000):**
   - Must listen on `0.0.0.0:8000`.
   - A `GET /pubkey` request must return the exact plaintext contents of your newly generated `/home/user/.ssh/id_ed25519.pub` file.
2. **TCP Authentication Service (Port 9000):**
   - Must listen on `0.0.0.0:9000`.
   - When a client connects and sends the exact transcribed PIN (as a UTF-8 string, with or without a trailing newline), the server must respond with the decrypted payload (as a UTF-8 string) and then close the connection.
   - If the client sends an incorrect PIN, it must respond with "ACCESS DENIED" and close the connection.

Ensure your Python server is running and bound to both ports before completing your task.