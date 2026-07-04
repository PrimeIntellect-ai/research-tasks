You are a deployment engineer tasked with diagnosing and fixing a user-level systemd service that refuses to start properly. 

A colleague created a service called `secure-app.service` which is supposed to run a small, secure web application locally. However, every time it tries to start, it crashes. Your colleague mentioned they were experimenting with systemd resource limits to simulate disk quotas and storage monitoring, and that the app also requires TLS to serve traffic securely, but they didn't finish the configuration.

Your tasks are to:

1. **Diagnose and Fix the Resource Limit**: 
   The service configuration is located at `/home/user/.config/systemd/user/secure-app.service`. The application script `/home/user/app/run.sh` is crashing immediately upon startup because it cannot write its initialization logs to `/home/user/app/logs/startup.log`. Identify which systemd directive is restricting the file size (simulating a storage quota limit), and modify the service file to remove this restriction entirely.

2. **Fix the Web Server TLS Configuration**:
   The script `run.sh` launches a Python-based HTTPS server on `127.0.0.1:8443`. However, the required TLS certificate (`cert.pem`) and private key (`key.pem`) are missing from the `/home/user/app` directory. Generate a new self-signed RSA 2048-bit certificate and unencrypted private key in the `/home/user/app` directory. Ensure the Common Name (CN) is set to `localhost`. Both files must be named `cert.pem` and `key.pem` respectively.

3. **Start the Service**:
   Apply your systemd configuration changes and successfully start the service using the user-level systemctl commands. Ensure the service stays in the `active (running)` state.

4. **Verify Connectivity**:
   Create a file at `/home/user/success.txt` that contains the HTTP response code obtained by querying the local web server using `curl`. You must query the server exactly at `https://127.0.0.1:8443` (ignoring certificate validation). The file should contain nothing but the 3-digit HTTP status code (e.g., `200`).

Ensure all files are owned by `user` and you do not use `sudo` or root privileges, as you only have access to your user environment.