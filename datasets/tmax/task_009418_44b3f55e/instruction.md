You are an IT support technician handling an escalated ticket from the Data Engineering team. They have a legacy log processing pipeline that is failing in multiple ways. 

**Ticket Details:**
"Our daily log aggregator script at `/home/user/log_pipeline/process_logs.sh` is broken. 
1. The helper utility fails to build.
2. Even when we bypassed the build, the pipeline produces a different number of output records than the input file contains.
3. Some usernames are being parsed incorrectly from the CSV (trailing whitespace/weird characters).
4. The final aggregated byte count in the summary is showing as a negative number, which is impossible."

**Your Objectives:**
1. Fix the build failure in the pipeline's directory.
2. Fix the Bash script (`/home/user/log_pipeline/process_logs.sh`) so that it:
   - Correctly handles the corrupted input formats (e.g., carriage returns) in `data/input.csv`.
   - Safely executes its concurrent background tasks without race conditions dropping or interleaving records in `output.txt`.
3. Fix the helper utility (`aggregator.c`) so it correctly calculates the total byte size without integer overflow.
4. Run the pipeline successfully. The script must output the final results to `/home/user/log_pipeline/summary.txt`.
5. Create a resolution report at `/home/user/log_pipeline/resolution_report.txt` containing strictly the final, correct total byte count on the first line.

**Constraints:**
- Do not remove the concurrency (background jobs `&`) in `process_logs.sh`, but fix the race condition causing data corruption when writing to `output.txt`. 
- Ensure your fixes are robust against DOS-style line endings (`\r\n`).