You are an automated backup operator building a sandbox to test application restores. We need a local environment that supervises the restored application, puts it behind a TLS-enabled proxy, and provides a CI/CD script to automate the restoration and verification process.

You do not have root access. You must use user-space tools and unprivileged ports. 

Please perform the following steps:

1. **TLS Configuration & Reverse Proxy**:
   - Generate a self-signed SSL certificate and private key in `/home/user/certs/` (name them `cert.pem` and `key.pem`).
   - Write a Python reverse proxy script at `/home/user/tls_proxy.py`. This proxy must listen on `127.0.0.1:8443` with TLS enabled (using your generated certificates) and securely forward all GET requests to `http://127.0.0.1:8080/`. Return the exact response body from the upstream server to the client.

2. **Process Supervision**:
   - We will use `supervisord` to manage the processes without root. 
   - Create a configuration file at `/home/user/supervisord.conf` that defines two programs:
     - `tls_proxy`: Runs your `/home/user/tls_proxy.py` script.
     - `app`: Runs `python /home/user/deploy/app.py` (which runs an HTTP server on port 8080).
   - Ensure the `supervisord.conf` is configured to run in user-space (store logs/pids in `/home/user/` so it doesn't require root permissions). Also configure a UNIX socket HTTP server in the conf so `supervisorctl` can connect to it.
   - Start `supervisord` in the background using this configuration.

3. **CI/CD Restore Pipeline Script**:
   - Write a Python script at `/home/user/cicd_restore.py` that accepts exactly one command-line argument: the path to a backup `.tar.gz` file.
   - When executed, this script must automate the restore process:
     1. Stop the `app` process using `supervisorctl` (pointing to your user-space config).
     2. Completely clear the contents of the `/home/user/deploy/` directory.
     3. Extract the provided `.tar.gz` backup file directly into `/home/user/deploy/` (so that `/home/user/deploy/app.py` exists).
     4. Start the `app` process using `supervisorctl`.
     5. Wait 2 seconds for the app to initialize.
     6. Make an HTTPS GET request to `https://127.0.0.1:8443/` (ensure you disable SSL verification in your HTTP client since it's a self-signed cert).
     7. Append the exact text response from the server into `/home/user/restore_log.txt` on a new line.

**Note:**
To help you develop, a mock backup already exists at `/home/user/archive/v1.tar.gz`. You can create this directory structure, extract it, and use it to test your supervisor and proxy setup before writing the CI/CD script.

Ensure that all services are running and that `python /home/user/cicd_restore.py /home/user/archive/v1.tar.gz` runs successfully end-to-end.