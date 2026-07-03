You are a Site Reliability Engineer (SRE). Your pager has been going off because the custom monitoring pipeline is falsely reporting 0.00% uptime for certain services, triggering critical alerts. 

The uptime calculation script is located in a Git repository at `/home/user/uptime-monitor/uptime_calc.sh`. The script takes two arguments: `<successful_requests>` and `<total_requests>`, and is supposed to output the uptime percentage formatted to two decimal places (e.g., `99.90`).

Recently, another engineer modified the script, and a regression was introduced causing severe precision loss (it truncates or zeroes out the percentage).

Your task is to:
1. **Find the regression:** Use `git bisect` to identify the exact commit that introduced the bug. Write the full 40-character SHA-1 hash of the bad commit to `/home/user/bad_commit.txt`.
2. **Fix the codebase:** Modify `uptime_calc.sh` on the `main` branch so that it correctly calculates the percentage to exactly two decimal places (e.g., `uptime_calc.sh 999 1000` must output `99.90`). Use standard CLI tools (like `awk` or `bc`).
3. **Write a regression test:** Create a Bash script at `/home/user/uptime-monitor/fuzz_test.sh` that generates random values for `successful_requests` and `total_requests` (where `0 < successful_requests < total_requests`) and runs `uptime_calc.sh`. The test should exit with code `1` if the output is strictly `0` or `0.00` (catching the precision loss bug), and exit with code `0` if the test passes (no zero-truncation). Make sure it is executable.

Ensure your fix is committed or left as a modified working tree on the `main` branch.