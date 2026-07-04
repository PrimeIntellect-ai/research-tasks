You are a DevOps engineer debugging a mathematically rigorous log processing pipeline that has started failing. You need to repair the environment, fix a vendored mathematical log aggregator, and create a robust shell sanitization filter.

Here are the details of the environment and what you need to do:

1. **Git Forensics & Configuration Repair**:
There is a local Git repository at `/home/user/pipeline-config`. Recently, a developer accidentally deleted a critical configuration file containing floating-point precision thresholds required by the pipeline. Search the Git history, recover the deleted file `math_thresholds.env`, and place it at `/home/user/pipeline-config/math_thresholds.env`.

2. **Vendored Package Debugging (Race Conditions & Spaced Filenames)**:
The system uses a third-party Bash package vendored at `/app/vendored/parallel-log-calc-1.0.4`. 
This package calculates high-precision latency sums across multiple log files in parallel. However, it is currently broken:
- It crashes or skips files when log filenames contain spaces.
- It suffers from a race condition when run with multiple workers, causing data corruption in its temporary mathematical accumulation files.
- It uses standard `awk` which suffers from floating-point precision loss on large numerical arrays (resulting in scientific notation rounding).
You must patch `/app/vendored/parallel-log-calc-1.0.4/bin/aggregate.sh` to correctly handle filenames with spaces, resolve the shared temporary file race condition, and replace the lossy `awk` addition with precise `bc -l` arithmetic.
Once fixed, run the aggregator on the directory `/home/user/test_logs` and save the exact output sum to `/home/user/aggregated_result.txt`.

3. **Adversarial Corpus Validation (Filter Creation)**:
We receive log files from untrusted distributed nodes. Some of these logs are maliciously crafted to exploit the aforementioned Bash vulnerabilities or inject mathematical anomalies (like `NaN`, `Infinity`, or extremely long scientific notations intended to trigger regex denial of service or calculation faults).
Write a Bash script at `/home/user/sanitize.sh` that takes a single file path as an argument.
- It must exit with code `0` (accept) if the file contains only valid numerical latency entries (lines with a timestamp and a valid positive decimal float up to 6 decimal places).
- It must exit with code `1` (reject) if the file is maliciously formatted, contains mathematical anomalies, or if the filename itself contains shell metacharacters/newlines designed to break shell scripts.

The automated test will invoke your script as `/home/user/sanitize.sh <path_to_log_file>`.