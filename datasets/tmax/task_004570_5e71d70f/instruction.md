You are a DevOps engineer tasked with debugging a critical data processing pipeline. 

We have a custom Go application located at `/home/user/log_processor.go`. This tool is designed to rapidly process a batch of log files located in `/home/user/logs/` concurrently and count the occurrences of different log levels (e.g., INFO, WARN, ERROR). The final aggregate counts are written to `/home/user/final_counts.json`.

However, the team has reported several critical issues:
1. **Inconsistent Results:** Running the tool multiple times on the exact same log files produces different counts for the log levels. You suspect a concurrency issue.
2. **Missing Data:** Even when counts seem somewhat correct, the total number of processed log lines is always slightly less than the actual number of valid lines in the log files. There might be an off-by-one or boundary condition bug in the log parsing logic.
3. **Application Crashes:** Yesterday, the application crashed silently when encountering a corrupted log entry. We captured a memory dump of the process right before the crash, located at `/home/user/crash.dump`. The team knows the corrupted string starts with the exact prefix `CRITICAL_CORRUPT: ` but they don't know the full string.

Your tasks are:
1. Analyze the memory dump `/home/user/crash.dump` to find the exact corrupted string. Extract the FULL string (including the prefix `CRITICAL_CORRUPT: ` and the alphanumeric code immediately following it) and save it to exactly `/home/user/corrupted_string.txt`.
2. Debug and fix `/home/user/log_processor.go` so that it safely and accurately processes all lines in the log files without dropping the last line of any file and without encountering race conditions.
3. Compile and run the fixed Go program. It should output the correct, consistent JSON summary of log level counts to `/home/user/final_counts.json`.

Ensure your fixes are robust and that running the program repeatedly always yields the exact same correct `final_counts.json`.