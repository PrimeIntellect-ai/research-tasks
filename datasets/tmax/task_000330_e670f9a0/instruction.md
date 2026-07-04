You are a cloud architect tasked with migrating a legacy service into a new high-availability architecture. As a transitional step, you need to implement a Python-based TLS API Gateway that also acts as a process manager for the backend worker processes (simulating our new lightweight containerized services).

Your objective is to create a fully functional, self-healing TLS reverse proxy and service manager in `/home/user/gateway.py`.

Here are the requirements:

1. **TLS Configuration**:
   - Create a directory `/home/user/certs/`.
   - Generate a self-signed RSA 2048-bit certificate (`cert.pem`) and private key (`key.pem`) in this directory without a passphrase. Use "Migration Gateway" for the Common Name (CN).

2. **Backend Services Setup**:
   - Create three directories: `/home/user/backend_9001`, `/home/user/backend_9002`, and `/home/user/backend_9003`.
   - In each directory, create a file named `health.txt` containing the word `OK`.
   - In each directory, create a file named `data.txt` containing the string `DATA FROM {PORT}` (e.g., `DATA FROM 9001`).

3. **Service Manager & Health Checks (`gateway.py`)**:
   - The script must spawn three child processes on startup. Each child process should run Python's built-in HTTP server on ports 9001, 9002, and 9003, serving their respective backend directories.
   - The script must implement a background thread/task that performs a health check every 2 seconds by making a GET request to `http://127.0.0.1:{port}/health.txt`.
   - If a health check fails (connection refused or non-200 status), the gateway must immediately kill the failed child process and spawn a new one for that port.
   - The gateway must append logs to `/home/user/gateway.log` with the exact format:
     `[HEALTH] Backend {port} is DOWN. Restarting...` whenever a restart occurs.
     `[HEALTH] Backend {port} is UP.` on the first successful health check after startup or restart.

4. **TLS Reverse Proxy (`gateway.py`)**:
   - The gateway must listen for HTTPS connections on `0.0.0.0:8443`, using the `cert.pem` and `key.pem` generated earlier.
   - Incoming GET requests to `https://localhost:8443/{path}` must be proxied to `http://127.0.0.1:{port}/{path}` using a simple round-robin selection among the *currently healthy* backends.
   - The response from the backend should be returned to the client.

To complete the task:
- Write all the necessary files.
- Run your `gateway.py` in the background (e.g., `python3 /home/user/gateway.py &`).
- Wait for it to initialize and verify its functionality. 
- Do not stop the `gateway.py` script once you have verified it is working; leave it running so the automated tests can evaluate the system state.