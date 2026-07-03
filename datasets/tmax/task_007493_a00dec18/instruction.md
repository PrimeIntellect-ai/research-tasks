You are a monitoring specialist tasked with setting up a local health check service that monitors a network target. You need to write a C program that performs a TCP health check, and write the corresponding systemd user unit files to manage its lifecycle.

Currently, we have a mock service called `target-server` that listens on TCP port 8080. We need a new service called `monitor` that checks if `target-server` is up. A common issue is the monitor service starting before the target server is ready, leading to false alerts. 

Perform the following steps:

1. **Write the Health Check Program in C**
   Create a C program at `/home/user/monitor.c` and compile it to `/home/user/monitor`.
   The program must:
   - Attempt a TCP connection to `127.0.0.1` on port `8080`.
   - Read the current time and format it according to the local timezone.
   - Append a line to `/home/user/monitor.log`.
   - If the connection succeeds, append: `OK: YYYY-MM-DD HH:MM:SS`
   - If the connection fails, append: `ALERT: YYYY-MM-DD HH:MM:SS`
   - Exit with code 0.

2. **Create systemd Unit Files**
   Create the systemd user unit configuration file for the monitor at `/home/user/systemd/user/monitor.service`.
   - It must be of `Type=oneshot`.
   - It must execute your compiled `/home/user/monitor` binary.
   - It must include the correct ordering directive so that it only starts *after* `target-server.service`.
   - It must enforce the timezone by setting the environment variable `TZ=Asia/Tokyo` directly within the unit file.

3. **Verify Configuration**
   To prove your C program works, start a temporary listener on port 8080 in the background (e.g., using `nc` or `python3 -m http.server 8080`), run your compiled `/home/user/monitor` binary with the environment variable `TZ=Asia/Tokyo` set to generate a successful log entry in `/home/user/monitor.log`, and then cleanly terminate your temporary listener.