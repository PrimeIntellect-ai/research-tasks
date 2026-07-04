You are a monitoring specialist tasked with implementing a staged deployment health checker. A newly migrated service uses a Blue/Green deployment strategy, and you need to build a custom C++ network monitor and a robust Bash wrapper script to handle the alerting and environment configuration.

There is a Python script located at `/home/user/mock_services.py` that mocks these services. When executed in the background, it spins up the Blue environment mock on port 9001 (which behaves normally) and the Green environment mock on port 9002 (which simulates a failure). 

Your objective is to complete the following tasks:

1. **Create the C++ Network Monitor**
   Write a C++ program at `/home/user/health_check.cpp`.
   - The program must read the target port from the environment variable `HEALTH_PORT`.
   - It should create a TCP socket, connect to `127.0.0.1` on the specified port, and send the string: `"STATUS_REQ\n"`.
   - It must read the response. If the response is exactly `"OK\n"`, the program should terminate with exit code `0`.
   - If the connection fails, times out, or the response is anything else, it must terminate with exit code `1`.
   - Compile this program to `/home/user/bin/health_check`. Create the `bin` directory if it does not exist.

2. **Setup Environment Profiles**
   Create two shell scripts to simulate the environment profiles:
   - `/home/user/env_blue.sh`: Must export `HEALTH_PORT=9001`
   - `/home/user/env_green.sh`: Must export `HEALTH_PORT=9002`

3. **Create the Robust Deployment Script**
   Write a bash script at `/home/user/deploy_monitor.sh`.
   - It must use robust error handling (e.g., `set -euo pipefail`), but ensure that a failure from the C++ monitor *does not* cause the bash script itself to crash.
   - It must accept exactly one argument representing the environment (`blue` or `green`).
   - It should source the corresponding environment file (e.g., `/home/user/env_blue.sh`).
   - It must execute the `/home/user/bin/health_check` binary.
   - Based on the exit code of the C++ program, it must append a log entry to `/home/user/deployment_alerts.log`:
     - On success (exit 0): `[INFO] Deployment <env> healthy on port <port>`
     - On failure (exit 1): `[CRITICAL] Deployment <env> failed network check on port <port>`
     *(Replace `<env>` with the argument provided, and `<port>` with the actual port number).*

4. **Execution and Verification**
   - Start the mock services in the background: `python3 /home/user/mock_services.py &`
   - Run your script for both environments:
     `/home/user/deploy_monitor.sh blue`
     `/home/user/deploy_monitor.sh green`
   - Ensure the `/home/user/deployment_alerts.log` file is correctly populated.