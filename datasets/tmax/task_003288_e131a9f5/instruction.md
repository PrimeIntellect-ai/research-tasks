You are a Site Reliability Engineer (SRE) tasked with monitoring the uptime of a legacy system that runs inside a QEMU virtual machine. The VM does not expose a modern API, but it does expose an interactive QEMU monitor over a UNIX domain socket.

Your objective is to automate the monitoring of this VM's uptime using Python and `pexpect`.

Currently, the QEMU monitor socket is located at `/home/user/qemu-monitor.sock`.

Please complete the following steps:

1. **Environment Setup:** 
   Add an environment variable `QEMU_MONITOR_SOCKET` pointing to `/home/user/qemu-monitor.sock` in `/home/user/.bashrc`. Ensure this is exported so future shell sessions can use it.

2. **Automated Monitoring Script:**
   Write a Python script at `/home/user/check_uptime.py`. This script must:
   - Read the socket path from the `QEMU_MONITOR_SOCKET` environment variable.
   - Use the `pexpect` library to spawn a connection to this socket using `nc -U <socket_path>`.
   - Interact with the socket to log in. The prompt will ask for `login: ` (use `sre_admin`) and `Password: ` (use `monitor123`).
   - Wait for the monitor prompt, which is exactly `(qemu) `.
   - Send the command `info uptime`.
   - Parse the output. The monitor will respond with a line containing the uptime (e.g., `VM uptime: 45 days, 12:00:00`) before returning to the `(qemu) ` prompt.
   - Send the command `quit` to exit cleanly.
   - The script must include robust error handling (e.g., if `nc` fails to connect or a timeout occurs).

3. **Output Generation:**
   The Python script must write the final parsed uptime directly to a log file at `/home/user/uptime_report.txt` in exactly this format:
   `STATUS: OK - Uptime: <extracted_uptime_string>`
   *(For example: `STATUS: OK - Uptime: 45 days, 12:00:00`)*

   If the script encounters any connection or expectation error, it should catch the exception and instead write:
   `STATUS: ERROR` to `/home/user/uptime_report.txt`.

Run your script once to generate the `/home/user/uptime_report.txt` file before finishing.