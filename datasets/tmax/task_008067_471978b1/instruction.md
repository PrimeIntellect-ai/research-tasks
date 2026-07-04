A customer has escalated a support ticket reporting that our sensor diagnostic pipeline occasionally fails. The pipeline calculates the cumulative moving average and standard deviation of high-frequency sensor readings. Most of the time it works perfectly, but for some datasets, the standard deviation outputs `nan` (Not a Number), which breaks downstream monitoring tools.

You are acting as the support engineer handling this escalation. 

The environment has two relevant files:
1. `/home/user/compute_stats.sh`: A bash script wrapping an `awk` program that processes numeric data line-by-line from standard input and prints the cumulative standard deviation.
2. `/home/user/sensor_data.csv`: A sample dataset provided by the customer (one numeric value per line) that triggers this issue.

Your objectives:
1. **Reproduce and Isolate (Delta Debugging):** The customer's file is large. Identify the *minimal contiguous subset* of lines from `/home/user/sensor_data.csv` that causes `./compute_stats.sh` to output `nan`. "Minimal contiguous subset" means the shortest possible sequence of consecutive lines from the original file that still produces at least one `nan` in the output. Save these exact lines to `/home/user/minimal_bug.csv`.
2. **Diagnose:** Determine the exact line number in the original `/home/user/sensor_data.csv` where the output *first* evaluates to `nan`. Write this line number to a file named `/home/user/bug_report.txt` in exactly this format:
   `Failing line: <line_number>`
   *(Note: 1-indexed, meaning the first line of the file is line 1).*
3. **Regression Testing:** Create a bash script `/home/user/regression_test.sh` that takes a filename as its first argument. The script should pass the contents of that file to `/home/user/compute_stats.sh`. If the output contains `nan`, the regression test script should print `BUG DETECTED` and exit with status code `1`. If the output contains valid numbers and no `nan`, it should print `PASS` and exit with status code `0`. Make sure this script is executable.

Do not modify `/home/user/compute_stats.sh` or `/home/user/sensor_data.csv`. Focus entirely on minimizing the test case, diagnosing the anomaly, and building the regression test.