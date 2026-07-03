You are a network engineer tasked with restoring a crucial connectivity diagnostic service that went down after a server migration. The original configuration files were lost, but a colleague saved a screenshot of the configuration schematic.

Your task involves extracting the configuration from this image, rebuilding the diagnostic service in Python, and deploying it with a proper directory structure and process supervisor.

Step 1: Configuration Extraction
We have a schematic image located at `/app/network_diag_schematic.png`. Use optical character recognition (OCR) to extract the text from this image. You will find three key configuration values:
- An HTTP listening port (e.g., `DIAG_PORT_HTTP=...`)
- A TCP listening port (e.g., `DIAG_PORT_TCP=...`)
- A secret authentication token (e.g., `SECRET=...`)

Step 2: Environment Setup
Create the following directory structure in the home directory exactly as specified:
- `/home/user/diag_service/bin`
- `/home/user/diag_service/logs`
- `/home/user/diag_service/run`

Create a symbolic link named `/home/user/diag_service/current_logs` pointing to the `/home/user/diag_service/logs` directory.

Step 3: Service Implementation
Write a Python script at `/home/user/diag_service/bin/diag_server.py` that implements a dual-protocol diagnostic server. The script must run concurrently and do the following:
1.  **HTTP Server:** Listen on `127.0.0.1` on the extracted HTTP port.
    *   It must have an endpoint `GET /status`.
    *   If the request includes the header `X-Diag-Secret` with the exact value of the extracted secret token, respond with HTTP status 200 and the JSON payload: `{"status": "UP"}`.
    *   If the header is missing or incorrect, respond with HTTP status 401.
2.  **TCP Echo Server:** Listen on `127.0.0.1` on the extracted TCP port.
    *   When a client connects, it must wait for a single line of text.
    *   If the first line is exactly `AUTH <secret>` (where `<secret>` is the extracted token), the server must echo back any subsequent lines of text sent by the client.
    *   If the first line is anything else, it must immediately close the connection.
3.  **Logging:** Both servers must append a log entry for every connection attempt to `/home/user/diag_service/logs/access.log`. The exact format of the log doesn't matter, but the file must be created and written to.

Step 4: Process Supervision
Write a bash script at `/home/user/diag_service/bin/start.sh` that acts as a simple process supervisor.
*   It must start `diag_server.py`.
*   It must redirect the standard output and standard error of the Python script to `/home/user/diag_service/logs/service.log`.
*   It must write the PID of the running Python process to `/home/user/diag_service/run/service.pid`.
*   If the Python process terminates for any reason, the supervisor script must automatically restart it.
*   Make sure `start.sh` is executable.

Step 5: Deployment
Run your `start.sh` script in the background so that the diagnostic service is active and listening on the required ports. Use tools like `curl` and `nc` or `telnet` to verify connectivity and functionality yourself.

Leave the service running in the background when you are finished.