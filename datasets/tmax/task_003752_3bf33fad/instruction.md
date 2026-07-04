You are a red-team operator simulating an attack against a custom file upload handler. The target application is vulnerable to a path traversal attack via ZIP file extraction, but it has a custom WAF (Web Application Firewall) that strictly validates uploaded files.

You must write a Python script at `/home/user/craft.py` that, when executed, generates a crafted payload file named `/home/user/payload.zip` satisfying all the following requirements to evade the WAF and trigger the vulnerability:

1. **Path Traversal Payload**: The ZIP file must contain a file with the exact name/path `../../../home/user/success.txt`. The content of this file must be the exact string `EXPLOIT_WORKED`. Note that standard Python `zipfile` might sanitize paths, so you must find a way to include the exact raw path in the ZIP directory structure.

2. **Dummy Certificate**: The target application expects a signed payload. You must generate a valid self-signed X.509 certificate (in PEM format) and include it in the ZIP archive under the filename `cert.pem`. The certificate must have the Common Name (CN) set to exactly `vulnerable.local`. The expiration date and other fields do not matter as long as it is a syntactically valid PEM certificate for that CN.

3. **Custom Hash Checksum**: The WAF verifies the integrity of the file. After the standard ZIP file is fully constructed, your script must compute the SHA-256 hash of the entire ZIP file. You must then append the 64-character lowercase hexadecimal string of that hash directly to the end of the file. (The WAF reads the last 64 bytes as the signature, removes it, and compares it against the SHA-256 hash of the remaining data).

Ensure your script runs successfully and completely autonomously to generate `/home/user/payload.zip` in the correct format. Standard libraries and `cryptography` are available in the environment.