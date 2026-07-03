You are an observability engineer working on optimizing a custom dashboard backend. Our dashboard heavily relies on a lightweight C++ metrics exporter, but we are currently facing a critical issue: the dashboard cannot scrape the metrics because of a network misconfiguration, and the exporter itself is suffering from severe performance degradation, causing scraping timeouts. 

You need to fix the codebase, deploy it as a managed service, and ensure it meets our strict latency and throughput requirements.

Here are your tasks:

1. **Fix the Vendored Package**:
   - The source code for the exporter is located at `/app/metrics-exporter`.
   - The dashboard attempts to scrape metrics from `127.0.0.1:8080`, but the server is currently hardcoded to bind to `127.0.0.2`. Update `server.cpp` to bind to `127.0.0.1`.
   - Inspect `server.cpp` for any artificial delays or inefficient blocking calls in the request loop that are causing high latency. Remove this perturbation so the server can handle requests at maximum speed.
   - Compile the binary using the provided `Makefile`. The output binary will be named `exporter`.

2. **Service Lifecycle Management**:
   - Create a local binary directory: `mkdir -p /home/user/bin` and copy the compiled `exporter` binary there.
   - Create a user-level systemd service file at `/home/user/.config/systemd/user/exporter.service`.
   - The service must execute `/home/user/bin/exporter`.
   - Process supervision: Configure the service to automatically restart on failure (`Restart=always`) with a 2-second delay (`RestartSec=2`).
   - Start and enable the service using `systemctl --user`.

3. **Staged Deployment Script**:
   - Write a deployment script at `/home/user/deploy.sh` (ensure it is executable).
   - The script should simulate a rolling deployment step. It must take exactly one argument (a version string).
   - The script must write this version string into `/home/user/version.txt`.
   - The script must then safely restart the `exporter.service` via `systemctl --user restart exporter.service`.

Once deployed, an automated testing tool will benchmark the endpoint at `http://127.0.0.1:8080/metrics`. To pass, your deployed service must achieve a throughput of at least 1000 requests per second.