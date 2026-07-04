You are a deployment engineer tasked with modernizing our legacy infrastructure monitoring stack. We are replacing a proprietary, undocumented compiled health-checker with a modern Python script, and exposing its output securely.

Step 1: Reverse Engineer the Legacy Checker
We have a stripped legacy binary located at `/app/legacy_health_checker`. It takes exactly 4 integer arguments representing system metrics:
`<disk_used_mb> <disk_total_mb> <ram_used_mb> <cpu_load_percent>`

For example: `/app/legacy_health_checker 50000 100000 8192 45`
It outputs a specific string format containing a health status and a calculated score. 
Your task is to reverse engineer the logic of this binary (using tools like `objdump`, `strings`, `ltrace`, or black-box testing) and write a bit-exact Python equivalent at `/home/user/new_health_checker.py`.
Your Python script must accept the same 4 positional CLI arguments and produce the exact same standard output as the legacy binary for any valid integer inputs. 

Step 2: System Monitor Wrapper
Write a bash script at `/home/user/monitor.sh` that gathers real-time system metrics and feeds them to your Python script. It must:
- Get disk used and total for the `/` partition (in MB).
- Get used RAM (in MB).
- Get the 1-minute CPU load average, multiplied by 100 to form an integer (e.g., 1.45 becomes 145).
- Invoke `python3 /home/user/new_health_checker.py` with these 4 values and print the result.

Step 3: Secure Web Server Setup
Expose the output of `/home/user/monitor.sh` over HTTPS on port 8443.
- Generate a self-signed TLS certificate and key at `/home/user/cert.pem` and `/home/user/key.pem`.
- Write a simple Python web server at `/home/user/server.py` that listens on `0.0.0.0:8443`, uses the generated TLS certificates, and upon receiving any GET request, executes `/home/user/monitor.sh` and returns its output as a plain text HTTP 200 response.
- Start this server in the background.

Constraints:
- Do not use root privileges (`sudo` is not needed).
- All paths must be exact.
- Ensure your Python checker is robust and handles the integer math exactly like the C binary (beware of division quirks!).