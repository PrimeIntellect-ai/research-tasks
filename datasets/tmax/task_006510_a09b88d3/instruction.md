You are a security engineer tasked with rotating credentials on a compromised Linux server. An attacker managed to steal a lower-privileged user's token, and you need to preemptively rotate the admin SSH keys by recovering the admin token from a weak custom token generation script.

Here is your objective:
1. Review the token generation script at `/home/user/token_generator.py` and the log file `/home/user/auth.log`.
2. Analyze the cryptographic weakness in the token generation process (predictable PRNG state) to recover the `admin` token that was generated immediately after the `guest` token.
3. Save the recovered admin token to a file at `/home/user/admin_token.txt`.
4. Generate a new Ed25519 SSH keypair for the admin user. Save the private key to `/home/user/.ssh/id_ed25519_admin` (do not use a passphrase).
5. Create a JSON file at `/home/user/key_rotation_payload.json` containing the recovered admin token and the new public SSH key. The format must be exactly:
```json
{
  "token": "<recovered_admin_token>",
  "ssh_key": "<content_of_public_key_file_without_trailing_newline>"
}
```

Constraints:
- You must perform all actions within `/home/user`.
- Ensure the SSH private key has the correct secure file permissions (0600).
- Do not modify the existing `/home/user/token_generator.py` or `/home/user/auth.log`.