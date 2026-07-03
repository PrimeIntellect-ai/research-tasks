You are acting as a security operator in a simulated red-team lab. You need to create a secure payload execution script that avoids command-line argument credential leaks (which would be visible in `/proc`) and securely connects to a local target service.

You are provided with the following files in `/home/user/`:
- `ca.crt`: A Certificate Authority public certificate.
- `server.crt`: A server certificate.
- `payload.b64`: A base64-encoded file containing an Ed25519 SSH private key.

Your task has two parts:

Part 1: SSH Service Hardening
Configure and start a local user-space SSH daemon.
1. Create a configuration file at `/home/user/sshd_config`.
2. Configure it to run on port `2222`.
3. Harden the configuration by explicitly disabling password authentication and enabling only public key authentication.
4. Set the host key file to `/home/user/ssh_host_ed25519_key` (you must generate this key without a passphrase).
5. Add the public key corresponding to the private key in `payload.b64` to `/home/user/.ssh/authorized_keys`. (You will need to decode `payload.b64` first to extract the private key, then generate its public counterpart).
6. Start the SSH daemon using the absolute path to `sshd` (e.g., `/usr/sbin/sshd -f /home/user/sshd_config`). 

Part 2: Payload Execution Script
Write a Python script at `/home/user/secure_runner.py` that does the following:
1. Validates the certificate chain by verifying that `/home/user/server.crt` is valid and signed by `/home/user/ca.crt`. You may use the `cryptography` Python package.
2. If the certificate is NOT valid, the script should exit with status code 1.
3. If the certificate is valid, read the base64-encoded SSH key from `/home/user/payload.b64` and decode it in memory (do not write the private key to a file if possible, or use a secure temporary file).
4. Connect via SSH to `127.0.0.1` on port `2222` as the user `user` using the decoded private key.
5. Execute the command `echo "ACCESS_GRANTED" > /home/user/loot.txt`.

Do not pass the SSH key or any credentials via command-line arguments in your Python script to avoid leaking them in `/proc`. Run your Python script to complete the exercise. The final verification will check for the existence and contents of `/home/user/loot.txt` and the hardness of your SSH config.