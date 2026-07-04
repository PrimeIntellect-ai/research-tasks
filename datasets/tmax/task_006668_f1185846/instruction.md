You are a Linux systems engineer tasked with hardening and fixing a broken local microservice configuration. A local Python backend service needs to securely access a restricted internal API and expose itself via a Unix domain socket, but the configuration is currently failing.

Your tasks are:

1. **SSH Tunneling**: An internal API is running on `127.0.0.2:8080`, which is strictly bound to that loopback interface. You must set up a persistent SSH tunnel in the background that forwards local port `9090` to `127.0.0.2:8080`. You can SSH to the local machine using `ssh -p 2222 user@127.0.0.1` (your SSH key is already configured at `/home/user/.ssh/id_rsa`).

2. **Environment Variable**: The backend application requires an environment variable to know where the tunneled API is. Add `export TUNNELED_API_URL=http://127.0.0.1:9090` to the file `/home/user/.bash_profile`. 

3. **Fix the Python Backend**: The backend application code is located at `/home/user/backend/app.py`. It currently crashes because it is attempting to bind its HTTP server to a Unix socket at `/var/run/backend.sock` (which you do not have permission to write to). Modify `/home/user/backend/app.py` so that it binds to `/home/user/backend.sock` instead. Once fixed, run the application in the background.

4. **Containerization Prep**: To prepare this app for deployment, write a standard `Dockerfile` in `/home/user/backend/Dockerfile`. It must use `python:3.10-slim` as the base image, copy `app.py` into `/app`, and set the command to run `python /app/app.py`.

5. **Verification Script**: Write a Python script at `/home/user/verify.py` that connects to the Unix domain socket at `/home/user/backend.sock`, makes an HTTP GET request to `/`, and reads the response body. The script must write the raw text response body to `/home/user/result.log`. Run this script so the log file is generated.