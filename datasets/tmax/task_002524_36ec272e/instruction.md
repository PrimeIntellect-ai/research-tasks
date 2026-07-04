You are a Site Reliability Engineer tasked with setting up a unified monitoring proxy for a legacy virtual machine environment. 

We have a proprietary, stripped binary located at `/app/qemu_probe`. This binary probes our QEMU instances to check their health, but it is notoriously finicky. It requires specific file permissions and environment variables to run successfully.

Your task is to create a Python service that safely wraps this binary, monitors local storage quotas, and exposes the data via multiple protocols for our internal dashboards.

Here are your specific requirements:

1. **Environment Setup:**
   - Create a directory `/home/user/monitor_data`.
   - Create a dummy state file at `/home/user/monitor_data/qemu_state.bin` containing exactly the string `QEMU_VNC_ACTIVE`.
   - The binary strictly enforces ACLs/permissions: `/home/user/monitor_data/qemu_state.bin` must have permissions set to exactly `0400`, otherwise the probe will crash.

2. **The Legacy Binary:**
   - The binary `/app/qemu_probe` requires the environment variable `PROBE_TOKEN` to be set to `sre_uptime_55`.
   - You must reverse engineer or experiment with `/app/qemu_probe` to figure out its required command-line arguments to read the state file you just created.

3. **The Multi-Protocol Python Service:**
   - Generate a self-signed TLS certificate and private key in `/home/user/certs/` (name them `server.crt` and `server.key`).
   - Write a Python script at `/home/user/sre_service.py` that runs continuously and listens on **two** ports simultaneously:
     - **Port 8443 (HTTPS):** An HTTPS web server. When a `GET` request is made to the `/health` endpoint, the Python script must execute `/app/qemu_probe` (with the correct token, arguments, and pointing to the state file) and return the binary's exact standard output as the HTTP response body with a 200 OK status code.
     - **Port 9090 (TCP):** A raw TCP socket. When a client connects and sends the exact string `STATUS\n`, the service must calculate the total disk space used by the `/home/user/monitor_data` directory. If the total size is less than or equal to 1048576 bytes (1MB), respond with `QUOTA_OK\n`. If it exceeds 1MB, respond with `QUOTA_EXCEEDED\n`. Close the connection after responding.

Run your Python script in the background before declaring the task complete. The automated verifier will connect to both port 8443 and 9090 to validate your implementation.