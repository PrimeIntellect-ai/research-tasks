You are acting as a security engineer tasked with rotating credentials and updating certificates for a local authentication service.

You need to perform the following steps to complete the credential rotation safely:

1. **TLS/SSL Certificate Management**: The current SSL certificate for our testing service has expired. Generate a new self-signed RSA 2048-bit X.509 certificate and private key. 
   - Save the certificate to `/home/user/new_cert.pem`
   - Save the private key to `/home/user/new_key.pem`
   - Set the validity to 365 days.
   - Set the Common Name (CN) to `test.local`. Do not set any other subject fields.

2. **Code Auditing & Sensitive Data Redaction**: We use a Python script at `/home/user/deploy_test.py` to deploy and test the new credentials. However, our automated vulnerability scanner flagged a potential CWE-532 (Insertion of Sensitive Information into Log File) vulnerability in this script.
   - Inspect `/home/user/deploy_test.py`.
   - Modify the script so that whenever it logs the authentication attempt, the actual password string is replaced with the exact string `***REDACTED***`.
   - The script must still log the username and URL normally.

3. **Authentication Flow Testing**:
   - Run the updated deployment script to test the new credentials: 
     `python3 /home/user/deploy_test.py --url https://test.local --user security_admin --pass "NewSecurePass2024!"`
     This will generate a log file at `/home/user/deploy.log`.
   - Finally, verify the new certificate and credentials by running the mock authentication flow test:
     `python3 /home/user/auth_test.py /home/user/new_cert.pem security_admin "NewSecurePass2024!"`
     This script will output `AUTH_FLOW_SUCCESS` to `/home/user/auth_result.txt` if the certificate and credentials are valid.

Ensure that `/home/user/deploy.log` does not contain the plaintext password, and that `/home/user/auth_result.txt` contains `AUTH_FLOW_SUCCESS`.