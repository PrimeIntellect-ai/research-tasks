You are acting as a security engineer responsible for analyzing authentication logs and rotating credentials for compromised service accounts.

We have an authentication log file located at `/home/user/auth.log`. The log entries are formatted as follows:
`[YYYY-MM-DD HH:MM:SS] user=<username> ip=<ip_address> event=<FAILED|SUCCESS>`

Your tasks are to:
1. **Intrusion Detection**: Analyze `/home/user/auth.log` using Python to identify compromised accounts. An account is considered compromised if it experiences a successful login (from an IP) that was immediately preceded by at least 3 failed login attempts from the *same* IP, for the *same* user, all occurring within a maximum sliding window of 60 seconds (inclusive of the first failure and the final success).

2. **SSH Key Management**: For each compromised user you identify, create a new Ed25519 SSH key pair without a passphrase. Save the private key to `/home/user/keys/<username>_id_ed25519` (ensure the `/home/user/keys` directory exists).

3. **Token Generation**: Generate a signed JWT-like access token for each compromised user to authorize the rotation. 
   - The Master Secret for signing is stored in `/home/user/master.secret`.
   - The header must be `{"alg": "HS256", "typ": "JWT"}`.
   - The payload must be `{"user": "<username>", "action": "key_rotation"}`.
   - Assemble the token as standard JWT: `base64url(header) + "." + base64url(payload) + "." + base64url(HMAC-SHA256(base64url(header) + "." + base64url(payload), secret))`. Remove any base64 padding (`=`).

4. **Output Generation**: Write a summary of your actions to `/home/user/rotation_summary.json`. The JSON file should be a dictionary where the keys are the compromised usernames, and the values are objects containing the exact full contents of the newly generated public key (`pub_key`) and the generated token (`token`).

Example format for `/home/user/rotation_summary.json`:
```json
{
  "compromised_user1": {
    "pub_key": "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAI... user@host",
    "token": "eyJhbGciOiAiSFMyNTYiLCAidHlwIjogIkpXVCJ9.eyJ1c2VyIjogImNvbXByb21pc2VkX3VzZXIxIiwgImFjdGlvbiI6ICJrZXlfcm90YXRpb24ifQ.signature..."
  }
}
```