You are a network security engineer investigating a series of suspicious file uploads on a compromised server. You have intercepted an image file from the attacker's traffic, located at `/app/intercepted_upload.png`. This image is a screenshot of the attacker's terminal and contains a highly sensitive, static "Upload-Token" that the backend temporarily uses to authorize uploads.

Your objective is to write a secure Python validation script at `/home/user/secure_upload.py` that will replace the compromised upload handler's logic. This script must validate incoming upload requests, check authorization, and strictly prevent path traversal vulnerabilities.

Your script must accept exactly three command-line arguments:
`python3 /home/user/secure_upload.py --path <requested_path> --token <provided_token> --cert <client_cert_pem_path>`

The script must implement the following logic in this exact order:

1. **Token Validation:**
   Extract the secret token from `/app/intercepted_upload.png` (you may use `tesseract` to read the image text). The token will be in the format `TOKEN: <string>`. 
   Compare the `--token` argument against this extracted token. If they do not match exactly, print `ERROR: INVALID_TOKEN` to stdout and exit with status code 1.

2. **Certificate Chain Validation:**
   The `--cert` argument provides a path to a client's PEM-encoded X.509 certificate. You must verify that this certificate is valid, not expired, and correctly signed by the internal Root CA located at `/app/root_ca.pem`.
   If the certificate is invalid, expired, or not verifiable against the root CA, print `ERROR: INVALID_CERT` to stdout and exit with status code 2.

3. **Intrusion Detection (Path Traversal):**
   The `--path` argument represents the filename or relative path the user wishes to upload to, which should be placed inside `/var/uploads/`.
   You must safely normalize this path and check for any path traversal attempts. Attackers may use URL-encoded characters (like `%2e%2e%2f` or `%2f`) or standard dot-dot-slash (`../`) sequences to escape the upload directory.
   If the normalized, decoded path attempts to write anywhere outside of the base directory `/var/uploads/`, or if it attempts to exploit traversal patterns to resolve to a higher directory before coming back down, print `ERROR: PATH_TRAVERSAL` to stdout and exit with status code 3.

4. **Success:**
   If all checks pass, construct the final absolute path. Print `SUCCESS: <absolute_path>` to stdout and exit with status code 0.

Ensure your Python script is robust and correctly handles edge cases. An automated fuzzer will test your script against thousands of malicious inputs and compare its output and exit codes against a heavily secured reference implementation.