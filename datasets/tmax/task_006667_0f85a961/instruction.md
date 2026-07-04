You are a Linux systems engineer performing an offline audit and diagnostic of a hardened server configuration. A user-level systemd service has been failing to start, likely due to a missing `After=` network dependency and potential storage constraints. You do not have root access, so the firewall rules and disk states have been exported for your review.

Your task is to write a Python script at `/home/user/diagnose.py` that automates the extraction of these configurations and performs an interactive diagnostic check.

The script must perform the following actions:
1. **Firewall Rule Extraction:** Parse the exported firewall rules in `/home/user/iptables.dump`. Find the TCP port number that is being forwarded (using DNAT) to `127.0.0.1:8080`. (Look for `--dport` and `--to-destination`).
2. **Storage Monitoring:** Parse the exported disk usage log at `/home/user/disk_usage.txt`. Find the usage percentage (as an integer) for the filesystem mounted on `/data`.
3. **Connectivity Diagnostics via Expect:** Use the Python `pexpect` module to spawn and interact with the local diagnostic tool `/home/user/check_service.sh`. You must pass the external port you found in step 1 as the first argument (e.g., `./check_service.sh 5522`). 
   - The script will prompt: `Enter Diagnostic PIN:`
   - You must send the PIN: `7788`
   - Capture the final status output by the script, which will be in the format `Status: <RESULT>`. Extract just the `<RESULT>` string.
4. **Report Generation:** Write the extracted data to `/home/user/summary.json` as a valid JSON object with the following exact keys and format:
   ```json
   {
     "external_port": 5522,
     "disk_usage_pct": 85,
     "service_status": "RESULT_HERE"
   }
   ```
   *(Note: `external_port` and `disk_usage_pct` must be integers, `service_status` must be a string).*

Make sure your Python script runs cleanly and produces the exact output format requested. You can use standard Linux text processing tools or Python to parse the files.