You are a security engineer tasked with rotating credentials and securing a web application after a recent breach. An attacker exploited a path traversal vulnerability in our Flask file upload handler. We have patched the vulnerability, but we need to rotate all potentially compromised credentials, verify the integrity of our stored files, and add an application-level firewall restriction.

Your task consists of the following phases:

**Phase 1: SSH Key Rotation**
The attacker may have stolen the SSH key used for deployments.
1. Generate a new Ed25519 SSH keypair without a passphrase, saving it to `/home/user/.ssh/id_ed25519`.
2. Delete the old compromised keypair (`/home/user/.ssh/id_rsa` and `id_rsa.pub`).
3. Replace the contents of `/home/user/.ssh/authorized_keys` so that it *only* contains the newly generated Ed25519 public key. Ensure the permissions of the `.ssh` directory and `authorized_keys` file are secure (700 and 600 respectively).

**Phase 2: File Integrity & Encryption Key Rotation**
The application stores uploaded files in `/home/user/app/uploads/`. These files are symmetrically encrypted using Fernet (from the `cryptography` library) with a key stored in `/home/user/app/old_key.key`.
1. Write a Python script at `/home/user/app/rotate_encryption.py`.
2. The script must read the old key, and decrypt every file in `/home/user/app/uploads/`.
3. Verify the integrity of each decrypted file by calculating its SHA-256 hash and comparing it to the original hashes stored in `/home/user/app/file_hashes.json` (a dictionary mapping filenames to their plaintext SHA-256 hex digests).
4. If a file's hash does not match, it has been tampered with. Write the filename (e.g., `file1.txt`) on a new line to `/home/user/app/tampered.log` and delete the tampered file from the `uploads` directory.
5. Generate a new Fernet key and save it to `/home/user/app/new_key.key`.
6. Re-encrypt all the *valid* files using the new key and save them back to `/home/user/app/uploads/` overwriting the old encrypted files.
7. Run your script.

**Phase 3: Application Network Policy**
The web app is located at `/home/user/app/app.py`. Modify `app.py` to implement an application-level firewall. 
1. Add a `before_request` hook in the Flask app that checks the requester's IP address (`request.remote_addr`).
2. If the IP address is NOT `127.0.0.1`, the app must abort the request with a `403 Forbidden` status code.

Ensure all tasks are completed correctly. Automated tests will verify the state of your SSH keys, check that `tampered.log` contains the correct tampered files, verify that the remaining files in `uploads` are successfully encrypted with `new_key.key`, and check the application source code for the IP restriction.