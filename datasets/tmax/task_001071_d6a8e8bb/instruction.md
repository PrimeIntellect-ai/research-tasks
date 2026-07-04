You are acting as an observability engineer trying to fix a flaky metrics collection stack. 

We have a custom C-based metrics aggregator that connects to a local telemetry server to pull dashboard data. Currently, our startup script (`/home/user/obs_stack/start.sh`) fails because the aggregator starts running before the telemetry server is fully bound to its port and before our user-space port forwarding is established. This is analogous to a missing `After=` dependency in systemd, but implemented via shell scripts.

Here is the setup in `/home/user/obs_stack`:
1. `telemetry_server.py`: A Python server that takes a few seconds to initialize and binds to port `9090`.
2. `aggregator.c`: A C program that attempts to connect to `127.0.0.1` on port `8080`, reads a single line of metrics, and writes it to `/home/user/obs_stack/dashboard.log`. It currently fails immediately if the port is not open.
3. `start.sh`: A script that launches the Python server in the background and then immediately launches the compiled aggregator.

Your tasks:
1. **Connectivity Diagnostics in C**: Modify `aggregator.c` so that instead of failing immediately, it retries the connection to `127.0.0.1:8080` up to 10 times, waiting 1 second between attempts. Once connected, it should read the data and write it to `/home/user/obs_stack/dashboard.log` in the format: `[SUCCESS] Metrics received: <data>`. Compile the modified code to an executable named `aggregator` in the same directory.
2. **User-Space Port Forwarding**: The telemetry server binds to port `9090`, but the aggregator is hardcoded to expect data on port `8080`. Modify `start.sh` to establish a user-space port forward using `socat` (forwarding TCP traffic from local port 8080 to local port 9090) in the background before the aggregator is executed.
3. **Process Ordering**: Ensure that `start.sh` correctly starts the Python server, sets up the `socat` port forwarding, and then executes the `aggregator`.

Execute your fixed `start.sh`. The task is complete when `/home/user/obs_stack/dashboard.log` is successfully created with the metrics data. Do not use root privileges.