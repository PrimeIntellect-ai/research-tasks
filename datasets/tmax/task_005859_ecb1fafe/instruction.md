You are a security engineer tasked with rotating the API credentials for a legacy internal service and securing its configuration.

The current credentials are in the file `/home/user/app_config/creds.json`. The JSON file contains a single key `api_key_b64`, and its value is a base64 encoded API token.

Perform the following tasks:
1. Read and decode the current token.
2. Generate a new token by computing the SHA256 hash of the decoded current token concatenated with the exact string `ROTATION_SALT_2024`. Calculate the hex digest of this hash.
3. Base64 encode this new hex digest and update `/home/user/app_config/creds.json` so the `api_key_b64` field contains this new base64 value. Keep it as valid JSON.
4. The current permissions on the credential file are too permissive. Change the file permissions of `/home/user/app_config/creds.json` to exactly `600` to prevent unauthorized access.
5. Create a Python script at `/home/user/verify_auth.py` that tests the authentication flow. The script must load `/home/user/app_config/creds.json`, decode the base64 token, and print exactly `Active Token: <decoded_hex_digest>` to standard output (where `<decoded_hex_digest>` is the raw hex digest of the new token).

Ensure your Python script runs without errors and correctly parses the JSON file.