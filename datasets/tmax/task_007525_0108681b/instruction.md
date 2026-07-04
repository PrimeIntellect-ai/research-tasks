You are a monitoring specialist tasked with automating network alerts and generating fallback routing configurations when a primary interface fails. Since you do not currently have root privileges to apply network changes directly, your automation must detect the failure, log an alert, and generate an executable remediation script for administrators to review and run.

Your task is to create a Python monitoring script and a shell setup script with the following precise specifications:

1. Create a Python script at `/home/user/generate_fallback.py`. This script must:
   - Read two environment variables: `PRIMARY_IFACE` and `FALLBACK_IFACE`. If either is missing, the script should exit with code 1.
   - Determine the status of the primary interface by reading the file `/sys/class/net/<PRIMARY_IFACE>/operstate`.
   - **If the primary interface file does not exist, or its content is anything other than `up`** (case-sensitive, ignoring leading/trailing whitespace):
     - Write the exact string `ip route replace default dev <FALLBACK_IFACE>` to the file `/home/user/remedy.sh`.
     - Make `/home/user/remedy.sh` executable (`chmod +x`).
     - Append the exact string `[ALERT] Primary down. Generated fallback to <FALLBACK_IFACE>.` followed by a newline to `/home/user/monitor.log`.
   - **If the primary interface is `up`**:
     - Ensure `/home/user/remedy.sh` exists but is completely empty.
     - Append the exact string `[OK] Primary active.` followed by a newline to `/home/user/monitor.log`.

2. Create a bash wrapper script at `/home/user/setup_monitor.sh`. This script must:
   - Export the environment variable `PRIMARY_IFACE` set to `dummy99` (an interface we expect to fail/not exist).
   - Export the environment variable `FALLBACK_IFACE` set to `lo`.
   - Execute the Python script `/home/user/generate_fallback.py`.

Once you have written both scripts, run `bash /home/user/setup_monitor.sh` to execute the monitoring run. Leave the resulting `monitor.log` and `remedy.sh` files on the filesystem for verification.