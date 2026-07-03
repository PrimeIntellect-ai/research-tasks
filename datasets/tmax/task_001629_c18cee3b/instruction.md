You are an operations engineer triaging an incident. A metric aggregation service has been crashing intermittently. The service calculates the standard deviation of network packet latencies using a Bash script. 

When the latencies are large, the service occasionally crashes, halting the pipeline. The system recently produced an error log and a partial memory dump from the time of the crash.

You have been provided with the following files in `/home/user/metrics/`:
1. `process_stats.sh`: The buggy bash script used to process metrics.
2. `error.log`: The captured standard error from the latest crash.
3. `mem.dump`: A binary/text memory dump taken right before the crash.

Your tasks are to investigate the statistical anomaly, extract the offending payload, reproduce the issue, and calculate the correct metrics.

Perform the following steps exactly as requested:

1. **Extract the Payload**: Analyze `mem.dump` (using tools like `strings` or `grep`) to find the exact batch of latency numbers that caused the crash. The numbers are stored in a buffer flanked by `[CRASH_CONTEXT] LAST_BUFFER:` and `[/CRASH_CONTEXT]`. Save these numbers to `/home/user/solution/payload.txt` (one number per line).

2. **Create a Minimal Reproducible Example (MRE)**: Write a bash script at `/home/user/solution/mre.sh` that reproduces the bug. It must pass the contents of `/home/user/solution/payload.txt` into the exact `awk` command found in `process_stats.sh`, so that running `./mre.sh` produces the same crash/warning seen in `error.log`. 

3. **Calculate the Correct Answer**: The bug is a mathematical precision anomaly known as catastrophic cancellation (occurring because standard double-precision floats in `awk` lose precision when summing squares of very large numbers). Calculate the correct standard deviation for the numbers in `payload.txt`. You must use a method that avoids precision loss (e.g., using `bc -l` for arbitrary precision, or an algorithm like Welford's method). Round the final standard deviation to exactly 4 decimal places (e.g., `1.2345`) and save this single number to `/home/user/solution/answer.txt`.

Constraints:
- Create the `/home/user/solution/` directory if it does not exist.
- Use only Bash shell built-ins, coreutils, and standard CLI tools (`awk`, `bc`, `grep`, `sed`, etc.). Do not use Python, Perl, or other scripting languages.
- Ensure your `mre.sh` has execution permissions.