You are a security engineer performing credential rotation and post-incident cleanup for a local web service. The service recently suffered from a path traversal vulnerability in its file upload handler, which resulted in some leaked credentials being written to the application logs. 

Perform the following security tasks using standard Linux CLI tools:

1. **TLS Certificate Rotation**: 
   Generate a new self-signed RSA 2048-bit X.509 certificate and private key in the directory `/home/user/certs/`. 
   - Name the certificate file `new_cert.pem` and the private key file `new_key.pem`.
   - The certificate must be valid for exactly 30 days.
   - Set the Common Name (CN) to `localhost` (you can leave other subject fields empty).

2. **File Permission and Access Control**:
   - For security, ensure that the newly generated private key (`/home/user/certs/new_key.pem`) has its file permissions strictly set to read-only for the owner, and no permissions for anyone else (octal `400`).

3. **Sensitive Data Redaction**:
   - The application log file located at `/home/user/logs/app.log` contains leaked API keys in the format `API_KEY=<secret_value>`. 
   - Read this file and redact the sensitive values so that every instance of an API key is replaced with the exact string `REDACTED` (e.g., `API_KEY=REDACTED`). 
   - Save the redacted output to a new file at `/home/user/logs/app_clean.log`. Do not modify the original log file.

4. **Exploit Payload Testing**:
   - To verify that the path traversal vulnerability scanner functions correctly in the upcoming test suite, craft a mock exploit payload.
   - Create a file at `/home/user/uploads/test_payload.txt`.
   - The file must contain exactly the following path traversal string (without a trailing newline if possible, or with one, but no other text): `../../etc/passwd`
   - Set the permissions of this mock payload file to read and write for the owner only (octal `600`) to ensure it cannot be accidentally executed.

Ensure all file paths are absolute and exactly match the requested names.