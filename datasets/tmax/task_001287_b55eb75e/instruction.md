You are a DevOps engineer investigating a suddenly failing CI pipeline for a log processing application. 

The application calculates an APDEX (Application Performance Index) score from server logs. Recently, the nightly batch job started failing because the APDEX calculation script is producing invalid scores (e.g., scores outside the valid 0.0 to 1.0 range). 

Here is what you know:
1. The repository is located at `/home/user/log_processor`.
2. The `HEAD` of the `main` branch is failing.
3. The tag `v1.0` is known to be a good, working state.
4. The script is invoked via `python3 process_logs.py <log_file>`. It prints the computed APDEX score to stdout.
5. The daily log file that triggers the bug is located at `/home/user/data/daily.log`. It contains 1000 lines. 
6. Only a very specific combination of log values triggers the invalid score due to a recent change in the formula implementation.

Your tasks are:
1. **Git Bisection**: Find the exact commit hash that introduced the bug.
2. **Delta Debugging**: Minimize the `/home/user/data/daily.log` file to the single offending log line that reproduces the invalid score issue when passed to `process_logs.py`. 
3. **Formula Correction**: Identify the mathematical error in the APDEX formula in `process_logs.py` at `HEAD` and correct it. The standard APDEX formula is: `(Satisfied Count + (Tolerating Count / 2.0)) / Total Samples`.
4. **Report**: Create a file at `/home/user/debugging_results.json` with the following strict JSON format:
```json
{
  "bad_commit": "<full_git_commit_hash>",
  "minimized_log_line": "<the_exact_single_line_from_the_log>",
  "corrected_formula_code": "<the_exact_single_line_of_code_you_replaced_it_with>"
}
```

Do not use root/sudo. Ensure your JSON is completely valid and properly escaped.