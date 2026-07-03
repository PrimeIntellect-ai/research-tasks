You are an edge computing engineer responsible for deploying a lightweight telemetry gateway on a fleet of IoT devices. The devices run a minimal Linux environment where you do not have root access. You need to automate the deployment process using bash.

We have pre-downloaded the source code for our proprietary gateway service to `/app/iot-gateway-2.1.0/`. However, the deployment needs manual intervention to work in an unprivileged environment, and you need to build the deployment pipeline script.

Your objective is to write and execute a Bash CI/CD script that fixes the package, installs it, configures user-space port forwarding (simulating edge NAT rules), and manages its lifecycle.

Complete the following steps:

1. **Fix the Vendored Package:**
   The package is located at `/app/iot-gateway-2.1.0/`. It uses a standard `Makefile`, but it is currently configured to install to a system-wide directory, which will fail because you do not have root access. Patch or modify the `Makefile` so that `make install` places the binary and assets into `/home/user/local/` instead. 

2. **Service Lifecycle & Environment:**
   The installed service executable will be at `/home/user/local/bin/gatewayd`. 
   - Write a supervisor bash script at `/home/user/supervisor.sh`. This script must start `gatewayd` in the foreground, trap exits, and infinitely restart `gatewayd` if it crashes, sleeping for 1 second between restarts.
   - `gatewayd` requires the environment variable `GATEWAY_AUTH_TOKEN` to be set to `edge2024`. If this is not set, the service will reject connections.
   - `gatewayd` will automatically bind to `127.0.0.1:8080`.

3. **Port Forwarding Simulation:**
   External telemetry sensors need to communicate with the gateway on port `9090`. Since you cannot configure `iptables`, use `socat` to create a user-space port forwarder. It must listen on TCP port `9090` (on all interfaces, i.e., `0.0.0.0`) and forward all traffic to the internal gateway at `127.0.0.1:8080`.

4. **CI/CD Deployment Script:**
   Create a master deployment script at `/home/user/deploy.sh` that automates this entire pipeline. When run, it should:
   - Perform the `make install` (assuming you've already patched the Makefile).
   - Start your `/home/user/supervisor.sh` in the background.
   - Start the `socat` port forwarding process in the background.

To complete the task, ensure that all scripts are written, executable, and that you have run `/home/user/deploy.sh` so that the gateway is actively listening on port `9090` via your `socat` forwarder.