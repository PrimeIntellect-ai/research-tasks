You are tasked with replacing a legacy configuration management monitoring tool with a fast, modern C++ implementation. 

We process configuration drift logs from our fleet. These logs are plain text files where each line represents a configuration change in the format:
`[YYYY-MM-DD HH:MM:SS] <SERVICE_NAME> <CONFIG_KEY>=<CONFIG_VALUE>`

A log file is considered "Clean" (safe to ingest) unless it hits one of two "Evil" criteria:
1. **Time-Series Anomaly:** The log contains too many changes in a short period. You must parse the timestamps and aggregate the number of configuration changes per hour (e.g., `2023-10-01 12:00:00` to `12:59:59` is one hour). If *any* single hour contains strictly more than 50 changes, the log is anomalous. 
2. **Secret Leakage:** The log contains exposed secrets in the `<CONFIG_VALUE>` field. We have lost the source code for the legacy checker, but the stripped binary is available at `/app/legacy_checker`. You must reverse-engineer this binary (e.g., using `strings`, `objdump`, or `gdb`) to discover the exact two secret detection patterns (regular expressions) it uses to flag lines.

**Your Goal:**
1. Reverse-engineer `/app/legacy_checker` to find the secret patterns.
2. Write a C++ program at `/home/user/detector.cpp`.
3. Compile it to `/home/user/detector`. (You may use standard C++17 features and `<regex>`).
4. The compiled executable must accept exactly one argument (the path to a log file).
   Example: `/home/user/detector /path/to/log.txt`
5. The executable must exit with code `0` if the log file is "Clean".
6. The executable must exit with code `1` if the log file is "Evil" (contains secrets or time-series anomalies).

Do not output anything to `stdout` or `stderr` in your final successful execution; the automated grading system will only look at the exit code. We have provided some sample logs in `/home/user/samples/` for you to test against, but the final evaluation will be run against a hidden corpus of clean and evil logs.