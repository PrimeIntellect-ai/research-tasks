I am a capacity planner analyzing resource usage on our internal nodes. I need a local metric exporter running securely, but I keep running into silent binding failures when trying to expose it. 

Please set up a reliable, secure local metric exporter in my home directory (`/home/user`) with the following requirements:

1. **Python Exporter**: Create a Python script at `/home/user/exporter.py`. It should start an HTTPS web server bound explicitly and exclusively to `127.0.0.1` on port `8443`.
2. **TLS Configuration**: Generate a self-signed SSL certificate and private key using OpenSSL (store them as `/home/user/cert.pem` and `/home/user/key.pem`). Configure your Python web server to use these for TLS.
3. **Capacity Payload**: Whenever an HTTP GET request is made to the server, it must respond with an HTTP 200 status code, a `Content-Type: application/json` header, and exactly this JSON payload:
   `{"cpu": 50, "mem": 1024}`
4. **Process Supervision**: To ensure the exporter stays up if it crashes, create a supervisor configuration file at `/home/user/supervisord.conf`. 
   - Define a program called `metric_exporter`.
   - Set it to execute your Python script.
   - Configure it to automatically restart if it exits unexpectedly (`autorestart=true`).
   - Route its stdout and stderr to `/home/user/exporter.log`.
5. **Execution**: Start the supervisor daemon using your configuration file in the background (e.g., `supervisord -c /home/user/supervisord.conf`). Do not use `systemd` or any root-level service managers.

Once you have completed this, verify your setup by ensuring `curl -k https://127.0.0.1:8443` returns the required JSON payload.