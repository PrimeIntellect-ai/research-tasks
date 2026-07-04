You are acting as a support engineer troubleshooting a bash log aggregation script that a customer reported is corrupting data. The script used to work correctly but has recently started producing invalid output.

The repository for the script is located at `/home/user/log_aggregator`.
The customer knows that the tag `v1.0` was working, and the current tag `v2.0` is broken. There is a test script `test.sh` provided in the repository that can be used to verify if the aggregation logic is working on a sample set of logs.

Your tasks are to:
1. **Find the Regression**: Use `git bisect` (using `test.sh` to determine commit status) to find the exact commit hash that introduced the bug.
2. **Debug and Fix**: Inspect the bad commit to understand what went wrong, and then fix the bug in `aggregate_logs.sh` on the current `master` branch.
3. **Add Assertions**: Modify `aggregate_logs.sh` to add an intermediate assertion right before it writes to `OUTPUT_FILE`. The assertion must verify that the `total_errors` variable is purely a non-negative integer (contains only digits). If it contains any non-digit characters (e.g., spaces, plus signs, etc.), the script must print an error message to standard error and `exit 2`.
4. **Collect Diagnostics**: After fixing the script, run it on the real customer logs located at `/home/user/actual_logs`. Write the output to `/home/user/aggregated_results.txt`.
5. **Create the Report**: Generate a final diagnostic report at `/home/user/diagnostic_report.txt` containing exactly two lines:
   - Line 1: The full Git commit hash of the first bad commit that introduced the bug.
   - Line 2: The calculated total number of errors found in `/home/user/actual_logs`.

Ensure you leave the system in a state where `aggregate_logs.sh` is fixed, executable, and contains the required assertion logic.