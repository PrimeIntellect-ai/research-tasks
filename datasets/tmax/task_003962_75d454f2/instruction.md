You are a Site Reliability Engineer (SRE) investigating an issue with an in-house uptime monitoring system. The system runs a Bash script that periodically checks services. Recently, the monitoring server has been crashing due to process exhaustion. It appears the monitoring script is leaking background processes when a service check times out and is cancelled (similar to a goroutine leak under cancellation, but in Bash).

Your environment is fully prepared in `/home/user/`.

**Phase 1: Log Timeline Reconstruction**
The monitoring system logs to three separate files in `/home/user/logs/`: `web.log`, `db.log`, and `api.log`.
1. Combine these three logs into a single chronologically sorted file at `/home/user/merged_timeline.log`.
2. The logs contain timestamps in the format `YYYY-MM-DD HH:MM:SS`. Sort them strictly by this timestamp.

**Phase 2: Minimal Reproducible Example (MRE)**
The monitoring script is located at `/home/user/monitor/uptime.sh`. It contains a function `check_service()` that simulates a network call (using `sleep`). When the timeout occurs, the script kills the backgrounded function, but orphaned child processes are left behind.
1. Write an MRE script at `/home/user/mre.sh` (using only Bash) that isolates and demonstrates this bug.
2. The script must source or copy the `check_service()` logic, trigger the cancellation exactly as it happens in the original script, and then output the number of orphaned `sleep` processes left running. 
3. The script should exit with code 0 if a leak is successfully demonstrated (count > 0).

**Phase 3: The Fix & Regression Test**
1. Create a fixed version of the monitoring script at `/home/user/monitor/uptime_fixed.sh`. You must modify the `check_service()` function or the cancellation logic so that when the check is cancelled, NO child processes (like `sleep`) are left orphaned.
2. Write a regression test at `/home/user/regression.sh`. This script must:
   - Run the fixed cancellation logic.
   - Verify that 0 orphaned `sleep` processes remain.
   - Exit with code 0 if the test passes (no leak), and code 1 if a leak is still present.

**Constraints & Rules:**
- You must use **Bash** and standard coreutils (e.g., `sort`, `awk`, `grep`, `ps`). Do not use Python, Perl, or other languages.
- Ensure all created scripts (`mre.sh`, `regression.sh`, `uptime_fixed.sh`) are executable (`chmod +x`).