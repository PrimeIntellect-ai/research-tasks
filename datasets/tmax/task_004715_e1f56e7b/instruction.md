You are tasked with diagnosing a sporadic build failure in a reporting tool. The repository is located at `/home/user/report-builder`. 

The team recently noticed that `./build_report.sh <logfile>` occasionally fails (returns a non-zero exit code). This is a regression; the script worked perfectly at the tag `v1.0`, but is failing on the `main` branch (which is about 200 commits ahead).

We suspect the failure is triggered by a statistical anomaly in the input log files (e.g., an unexpected ratio of certain log levels), but we don't know the exact condition. 

Your tasks are:
1. **Fuzz Testing**: Write a fuzzer script (e.g., `fuzz.sh`) in Bash that generates random log files. Each line in the generated log file should randomly be either an `INFO` or `ERROR` message (e.g., `[INFO] Request processed` or `[ERROR] Connection timeout`). 
2. **Statistical Anomaly Investigation**: Use your fuzzer to discover what statistical distribution of `INFO` vs `ERROR` lines causes `./build_report.sh` to crash on the `main` branch. Ensure your fuzzer can reliably trigger the failure.
3. **Automated Bisection**: Use `git bisect` in conjunction with a wrapper around your fuzzer to automatically find the exact commit that introduced the regression between `v1.0` and `main`.
4. **Reporting**: Once you have identified the exact bad commit, write the full 40-character Git commit hash to `/home/user/bad_commit.txt`. 

Requirements:
- Do not modify the history of the repository.
- The repository is at `/home/user/report-builder`.
- The final state must include the correct commit hash in `/home/user/bad_commit.txt`.
- Your bisection script must properly handle exit codes to guide `git bisect run`.