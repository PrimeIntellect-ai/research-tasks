You are an operations engineer triaging an incident. A data processing bash script, `/home/user/process_logs.sh`, is meant to process several log files in parallel, calculate the total number of errors, and generate an overall error rate report. However, the script is currently failing, hanging indefinitely, and producing incorrect results.

Your objective is to debug and fix the script so it correctly processes the log files located in `/home/user/logs`.

Here are the specific issues you need to investigate and resolve:
1. **Environment & Pathing Issues**: The script is not finding the log files correctly, and it assumes certain directories exist which may not. You must repair these environment and path assumptions.
2. **Concurrency Hang (Deadlock)**: The script uses background jobs to process files in parallel and a directory-based lock to safely update a shared total. However, the script hangs forever when multiple jobs run. Use state tracing to identify why the background jobs are deadlocked and fix the lock release mechanism.
3. **Formula Correction**: Even when the script runs, the final calculated total number of errors and the resulting error rate are mathematically incorrect. Fix the formulas used to accumulate the errors.

Requirements:
- Do not remove the parallelization (the `&` and `wait` logic must remain).
- The logs are located in `/home/user/logs`.
- Save your fully corrected script to `/home/user/process_logs_fixed.sh`.
- Execute your fixed script. It must successfully produce the file `/home/user/final_report.txt` containing the exact string `Rate: X` (where X is the correct integer percentage of lines that contain the word "ERROR").

Fix the script and run it to produce the correct final report.