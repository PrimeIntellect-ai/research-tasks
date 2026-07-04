You are a network engineer analyzing intercepted web traffic to identify a hidden malicious endpoint. You have captured an encrypted authentication token, but you need to decrypt and validate it to extract the target URL. 

You have the following files on your system:
- `/home/user/intercepted_token.txt`: Contains the encrypted authentication token (in base64 format).
- `/home/user/auth_key.key`: Contains the symmetric encryption key used by the web service.

Perform the following steps:
1. **Fix File Permissions**: Security best practices dictate that the symmetric key file must be strictly read-only for the owner (i.e., `0400`). Set the correct permissions on `/home/user/auth_key.key`.
2. **Decrypt the Token**: Write a Python script at `/home/user/analyze.py` that reads the key and uses the `cryptography.fernet.Fernet` module to decrypt the contents of `/home/user/intercepted_token.txt`.
3. **Validate the Payload**: The decrypted token is a JSON string containing the following keys: `user`, `role`, `next_endpoint`, and `checksum`. 
4. **Verify the Checksum**: The `checksum` field represents the hex digest of the SHA-256 hash of the `next_endpoint` string. Your Python script must calculate the SHA-256 hash of the extracted `next_endpoint` and compare it against the `checksum` value in the JSON object.
5. **Log the Result**: 
   - If the calculated hash matches the `checksum`, write exactly the value of `next_endpoint` to a new file at `/home/user/investigation_result.log`.
   - If the hash does NOT match, write the exact word `CORRUPTED` to `/home/user/investigation_result.log`.

Do not add any additional text, newlines, or formatting to `/home/user/investigation_result.log` other than the requested string.