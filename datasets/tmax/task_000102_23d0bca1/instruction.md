You are an engineer diagnosing why a deployed Python web service fails to start. 

The application is located at `/home/user/server.py` and reads its configuration from `/home/user/config.json`. When attempting to run the server, it immediately exits and logs the failure to `/home/user/server.log`. 

Your task is to fix the deployment:
1. Inspect the configuration and log files to determine why the server is crashing.
2. Resolve the TLS certificate errors by generating a self-signed certificate (`/home/user/cert.pem`) and an unencrypted private key (`/home/user/key.pem`) using standard `openssl` commands.
3. The server is currently configured to bind to a privileged port, which will fail without root access. Use a text processing tool (like `sed`, `awk`, or `jq`) to update `/home/user/config.json` so that the `port` value is changed to `8443`.
4. Start the server in the background (`python3 /home/user/server.py &`).
5. Verify the service is running by executing `curl -k -s https://localhost:8443/health` and redirect the output to `/home/user/health_check.txt`.

Ensure that:
- The configuration file is valid JSON after your edits.
- The server is successfully listening on port 8443.
- The output in `/home/user/health_check.txt` exactly matches the health endpoint response.