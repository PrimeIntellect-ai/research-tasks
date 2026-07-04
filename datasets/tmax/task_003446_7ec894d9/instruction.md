You are assisting a security auditor in setting up a secure, automated data processing service. You must complete a multi-stage workflow involving fixing a vendored auditing package, creating a secure API for file integrity checks, and configuring a hardened SSH access point.

**Step 1: Fix the Vendored Package**
A local Python package is provided at `/app/vendored/py-auditor-1.2.0`. It contains a function `get_file_hash(filepath)` in `py_auditor/hasher.py`. 
Currently, it has a bug where it incorrectly uses MD5.
1. Modify `py_auditor/hasher.py` so that `get_file_hash` computes and returns the hex digest of the file using **SHA-256**.
2. Install this package in your Python environment.

**Step 2: Create the Auditor HTTP Service**
Write a Python HTTP server (e.g., using the built-in `http.server` or a microframework like Flask/FastAPI if you install it) and save it as `/home/user/server.py`.
The service must:
1. Listen on `127.0.0.1:8000`.
2. Provide a `POST /audit_file` endpoint that accepts a JSON payload: `{"path": "/absolute/path/to/file"}`.
3. Check the file permissions of the requested file. 
   - If the file permissions are NOT exactly `0600` (read/write for owner only), the endpoint must return an HTTP 403 status code with the JSON response: `{"error": "Invalid permissions"}`.
   - If the file permissions are exactly `0600`, the endpoint must read the file, compute its hash using the `get_file_hash` function from the `py_auditor` package, and then **encrypt** the resulting hex string.
4. **Encryption requirements:** Encrypt the hex string using AES-GCM (you may `pip install cryptography`). Use the 32-byte AES key stored in `/app/aes_key.bin`. Use a fixed 12-byte initialization vector (IV) consisting of all zeros (`b'\x00' * 12`). Return an HTTP 200 status code with the JSON response: `{"encrypted_hash": "<base64_encoded_ciphertext_including_tag>"}`. (Append the 16-byte authentication tag to the ciphertext before base64 encoding).
5. Run this server in the background.

**Step 3: SSH Hardening**
The auditor needs to access this service securely via SSH port forwarding.
1. Configure an SSH server (`sshd`) to run locally.
2. Ensure it listens on `127.0.0.1:2222`.
3. Disable `PasswordAuthentication`.
4. Ensure the auditor's public key, located at `/app/auditor_id_rsa.pub`, is added to the `user` account's authorized keys so they can log in without a password.
5. Start the SSH service in the background (you can run it using `/usr/sbin/sshd -p 2222 -f /home/user/sshd_config` or similar user-space methods, ensuring you generate necessary host keys).

Ensure both the HTTP server and the SSH server are running.