You are a security engineer tasked with rotating credentials on an internal system. The previous administrator left behind a legacy credential management service and a locked SSH configuration. 

You must perform the following steps to regain control and rotate the SSH keys:

1. **Service Auditing:** A legacy configuration service is running locally on a TCP port somewhere between `8000` and `8050`. Find the service.
2. **Credential Extraction:** Once you find the service, make a GET request to its `/config` endpoint. It will return a JSON payload containing an `admin_hash` (a SHA-256 hash of the legacy administrator password).
3. **Password Cracking:** A list of potential legacy passwords is located at `/home/user/legacy_passwords.txt`. Write a Python script to hash the words in this dictionary and compare them to the extracted `admin_hash` to crack the password.
4. **SSH Hardening & Rotation:** An automated key rotation script is located at `/home/user/rotate_ssh.py`. You must run this script, passing the cracked password via the `--password` argument (e.g., `/home/user/rotate_ssh.py --password <YOUR_CRACKED_PASSWORD>`). 
   - If the password is correct, the script will automatically generate a new secure Ed25519 SSH keypair, harden the `/home/user/.ssh/authorized_keys` file by replacing its contents with the new public key, and set the correct permissions. The new private key will be saved to `/home/user/.ssh/id_ed25519`.
5. **Verification:** Calculate the SHA-256 checksum of the generated *private* key (`/home/user/.ssh/id_ed25519`).
6. **Reporting:** Create a JSON file at `/home/user/rotation_summary.json` containing the cracked password and the SHA-256 checksum of the new private key. The file must strictly follow this format:
```json
{
  "cracked_password": "the_plaintext_password",
  "private_key_checksum": "sha256_hex_digest_of_the_private_key"
}
```

Constraints:
- You must use Python to write the cracking script.
- Do not modify `/home/user/rotate_ssh.py`.