You are a Site Reliability Engineer (SRE) investigating an issue with a custom Bash monitoring agent. 

A legacy uptime calculation script located at `/home/user/uptime_monitor.sh` reads base64-encoded ping logs from `/home/user/logs/ping_data.b64`. The decoded logs contain CSV data in the format `timestamp,status` (where a status of `1` means UP and `0` means DOWN).

Currently, running `/home/user/uptime_monitor.sh` fails to produce the correct uptime percentage. It seems to be suffering from multiple issues:
1. A dependency conflict or bad binary shadowing a standard system tool, causing silent failures or errors.
2. A hidden encoding/serialization issue in the decoded log data that prevents accurate status parsing.
3. A logical bug in the bash arithmetic formula used to calculate the uptime percentage (resulting in 0%).

Your task is to debug and fix `/home/user/uptime_monitor.sh` so that it accurately calculates the uptime percentage as a whole number and writes it to `/home/user/uptime_report.txt`. 

Requirements:
- Fix the script in place (`/home/user/uptime_monitor.sh`).
- Do not hardcode the final answer; the script must calculate it dynamically from `/home/user/logs/ping_data.b64`.
- The final output in `/home/user/uptime_report.txt` should be in the exact format: `Uptime: X%` (where X is the correct integer percentage).
- Use standard bash tools. You can use tools like `strace` or `bash -x` to trace the system calls and variable states if needed.