You are a DevSecOps engineer implementing "policy as code" for a new microservice. Your goal is to write a Python script that acts as an automated security scanner to verify that the service meets our baseline security requirements before it can be deployed.

A pre-release version of the service is located at `/home/user/app/`.
First, start the application in the background by running:
`python3 /home/user/app/server.py &`
This will start a local HTTPS server on `https://127.0.0.1:8443`. Note that it uses a self-signed certificate.

You need to write a Python script at `/home/user/policy_check.py` that performs the following security checks against this running server:

1. **TLS/SSL Validation**: Extract the SSL certificate from the running server at `127.0.0.1:8443`. Check if the `subjectAltName` (SAN) extension contains `DNS:localhost`. 
2. **Authentication Flow Testing**: Send an HTTP POST request to `https://127.0.0.1:8443/api/auth` with the JSON payload `{"user": "admin", "pass": "admin"}`. Verify that the server correctly rejects default/weak credentials by returning an HTTP 401 Unauthorized status code.
3. **Vulnerability Scanning (Path Traversal)**: Send an HTTP GET request to `https://127.0.0.1:8443/public/..%2f..%2f..%2fetc%2fpasswd`. Verify that the server is not vulnerable to directory traversal (it should NOT return an HTTP 200 OK status).

Your script must run these checks and output the results to a JSON file located at `/home/user/policy_report.json`.
The JSON file must have the exact following schema:
```json
{
  "tls_san_valid": true,
  "auth_secure": true,
  "path_traversal_secure": true
}
```
Set the boolean values to `true` if the check passes (i.e., SAN contains localhost, auth returns 401, and path traversal does not return 200), and `false` otherwise.

Run your script to generate the `/home/user/policy_report.json` file. Ensure that your script correctly handles the self-signed certificate when making HTTP requests (e.g., by disabling certificate verification in your HTTP client, since this is a local dev environment).