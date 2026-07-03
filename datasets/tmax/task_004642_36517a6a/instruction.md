We are building a lightweight Python-based "Manifest Controller" to act as a mock Kubernetes operator for local development. This operator will secure our local manifest files, back them up, and serve a status endpoint over HTTPS.

Please perform the following tasks in the `/home/user` directory:

1. **Permission Management:**
   There is a directory at `/home/user/manifests`. Secure this directory by changing its permissions so that ONLY the owner has read, write, and execute permissions (no access for group or others).

2. **TLS Certificate Generation:**
   Create a directory `/home/user/certs`. Generate a self-signed RSA (2048-bit) TLS certificate and private key using `openssl`. 
   Save the certificate as `/home/user/certs/cert.pem` and the private key as `/home/user/certs/key.pem`. Use no passphrase and dummy subject values.

3. **Backup & Web Server (The Operator):**
   Write a Python script at `/home/user/operator.py`. When run, this script must:
   - Create a compressed tarball archive (`.tar.gz`) of the `/home/user/manifests` directory and save it as `/home/user/backups/manifests.tar.gz`. (Assume the `/home/user/backups` directory already exists).
   - Start an HTTPS web server on `127.0.0.1` port `8443` using the certificate and key you generated.
   - For any GET request, the server must respond with HTTP status 200 and the exact plaintext string: `Backup successful: manifests.tar.gz`.
   - Use Python's built-in `http.server` and `ssl` modules.

4. **Execution and Verification:**
   - Run your `operator.py` in the background.
   - Once it is running, use `curl` to make a GET request to `https://127.0.0.1:8443`, ignoring certificate warnings.
   - Save the output of the curl command to `/home/user/status.log`.