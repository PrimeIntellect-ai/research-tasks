You are a security engineer tasked with rotating credentials for an internal data processing tool. During a routine audit, you lost access to the new staging credential, but you noticed a vulnerability in the tool's JWT validation implementation that you can use to recover it.

The tool is a Python script located at `/home/user/app/verify_data.py`. It accepts a JWT as a command-line argument. If the JWT is valid and the token's payload indicates the user has the `admin` role, the script prints out the new staging credential.

Your tasks are:
1. Analyze `/home/user/app/verify_data.py` to understand its JWT validation logic. You will notice it handles the `none` algorithm improperly.
2. Craft a forged JWT that bypasses the signature verification and grants you the `admin` role. The payload must contain the JSON key `"role"` set to `"admin"`.
3. Execute the script using your forged JWT to extract the staging credential.
4. Save the exact extracted credential (without any extra text or newlines) into a file located at `/home/user/recovered_credential.txt`.
5. Compute the SHA-256 hash of the recovered credential (ensure no trailing newline is included in the hash computation) and save the hash value in hex format to `/home/user/credential_hash.txt`.

Ensure the final files `/home/user/recovered_credential.txt` and `/home/user/credential_hash.txt` contain only the required values.