You are a DevSecOps engineer tasked with enforcing policy as code by building a custom vulnerability scanner. A development team has committed configuration files that may contain hardcoded authentication tokens. Your goal is to scan these files, verify if the tokens are active, and securely report the active ones.

You are provided with the following environment:
1. `/home/user/repo/`: A directory containing various `.conf` files.
2. `/home/user/auth_mock.py`: A local mock authentication service script. You can test a token by running `python3 /home/user/auth_mock.py <base64_token>`. It will exit with status code `0` if the token is valid and active, and `1` if it is invalid.
3. `/home/user/fernet.key`: A file containing a valid `cryptography.fernet` symmetric key.

Your task is to write and execute a Python script that does the following:
1. Scans all `.conf` files in `/home/user/repo/` for lines that start exactly with `Authorization: Basic ` followed by a base64 encoded token.
2. Tests each extracted base64 token against `/home/user/auth_mock.py`.
3. If the mock service confirms the token is valid (exit code 0), decode the base64 payload to reveal the underlying `username:password` string.
4. Encrypt the decoded `username:password` string using the Fernet key provided in `/home/user/fernet.key`.
5. Write the results to a JSON file at `/home/user/secrets_report.json`.

The output file `/home/user/secrets_report.json` must have the following exact format:
```json
[
  {
    "file": "app1.conf",
    "encrypted_secret": "<fernet_encrypted_string_here>"
  },
  ...
]
```
The list must only contain entries for **valid** tokens and must be sorted alphabetically by the `"file"` name (just the base filename, e.g., `app1.conf`). Ensure you use the `cryptography` library for the Fernet encryption.