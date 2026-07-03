You are a penetration tester conducting an assessment of a local service. Your objective is to validate the service's cryptographic identity, analyze its authentication flow for injection vulnerabilities, and extract a highly privileged access token.

The target environment is located in `/home/user/target_env`.

Follow these exact steps:

1. **Certificate Validation**: 
   The target's public certificates are stored in `/home/user/certs/`. You must cryptographically verify that `server.crt` was signed by `ca.crt`. Write the result to the first line of `/home/user/pentest_report.txt` exactly in the format: `CERT_STATUS: VALID` or `CERT_STATUS: INVALID`.

2. **Service Initialization**:
   The target application is a Python web service located at `/home/user/target_env/server.py`. 
   Install necessary dependencies (it requires `flask`) and start the application in the background. It will bind to `127.0.0.1:8080`.

3. **Vulnerability Analysis & Authentication Testing**:
   The application exposes a login endpoint at `POST http://127.0.0.1:8080/auth`. It accepts a JSON payload containing `username` and `password`.
   Automate a scan or manually review the provided `server.py` to identify an injection vulnerability in the authentication flow.

4. **Exploitation**:
   Write a Python script (or use curl) to exploit the injection vulnerability to bypass the authentication mechanism and log in as the `admin` user without knowing their actual password.
   If successful, the endpoint will return a JSON response containing a secret access token.

5. **Reporting**:
   Append the extracted token to the second line of `/home/user/pentest_report.txt` exactly in the format: `TOKEN: <extracted_token_here>`.

Do not modify the `server.py` application code. All your work should be done using standard shell tools and Python scripts. Ensure the report file is exactly two lines long and matches the requested formatting.