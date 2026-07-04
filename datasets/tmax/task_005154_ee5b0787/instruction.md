You are a Site Reliability Engineer (SRE) investigating an uptime monitoring service that recently started deadlocking under high contention due to a suspected precision loss in its calculations. 

We have isolated a few artifacts for your investigation:
1. `/app/dashboard_alert.png` - A screenshot of the SRE alert dashboard showing the exact fatal error code triggered during the deadlock.
2. `/app/monitor.dump` - A partial memory dump (in binary/text format) taken at the time of the crash. 
3. `/app/uptime-monitor` - A local Git repository containing the Bash-based uptime calculation service.
4. `/app/oracle_uptime_calc` - A stripped, known-good reference binary from a reliable older system.

Your task has the following stages:

**1. Memory Analysis & Alert Identification:**
Extract the fatal error code from `/app/dashboard_alert.png` (using OCR tools like `tesseract`). Search for this exact error code within `/app/monitor.dump` to find the associated precision loss signature (a specific string formatted as `PRECISION_THRESHOLD=<value>`).

**2. Git Bisection & Regression Testing:**
Navigate to `/app/uptime-monitor`. This repository contains a script `calc.sh`. Over its commit history, a precision loss bug was introduced that triggers the deadlock when processing values matching the `PRECISION_THRESHOLD` signature. Write a regression test using the threshold you found, and use `git bisect` to identify the commit hash that introduced the bug. 

Write the bad commit hash to `/home/user/bad_commit.txt`.

**3. Fix and Re-implement:**
Create a fixed version of the uptime calculator at `/home/user/fixed_uptime_calc.sh`.
This Bash script must take a single file path as an argument. The file will contain a list of integers (one per line) representing daily uptime in seconds.
Your script must calculate the overall uptime percentage (Total Uptime / (Number of days * 86400) * 100) and output it to standard output.
You must ensure arbitrary precision to avoid the deadlock bug. Your script's output must be **BIT-EXACT** equivalent to the output of the reference oracle `/app/oracle_uptime_calc` when provided the same input files. 
Your script should be executable (`chmod +x`).