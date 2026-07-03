You are acting as a Support Engineer tasked with diagnosing a crash in a customer's custom log transformation utility. The customer reported that their data pipeline fails abruptly when processing a specific batch of logs, but they cannot identify which log entry is causing the issue or why.

The source code for the utility is located at `/home/user/log_transformer.c`.
The large log file causing the crash is located at `/home/user/large_log.txt`.

Your tasks are:
1. **Compilation**: Compile the C program with debugging symbols enabled into an executable named `log_transformer` in `/home/user/`.
2. **Crash Analysis**: Run the utility against `/home/user/large_log.txt`. It will crash (Segmentation fault). Use standard tools (like `gdb` or `valgrind`) to analyze the crash and determine the exact C function in `log_transformer.c` where the invalid memory access originates (ignore standard library functions like `strlen` or `__GI_strlen` in your final report; we want the highest-level function in *our* source code that caused the bad call).
3. **Test Minimization (Delta Debugging)**: The log file contains thousands of lines. Use shell commands (like `head`, `tail`, `sed`, `split`, etc.) to isolate the single minimal test case—the exact single line of log text—that triggers the crash.
4. **Data Transformation Diff**: To help the dev team understand the expected state prior to the crash, identify the line *immediately preceding* the crashing line in the original `large_log.txt`, and determine what its successful JSON transformation looks like.

Finally, compile your findings into a diagnostic report at `/home/user/diagnostic_report.txt` with exactly three lines in the following format:
Line 1: Function: [Name of the function in log_transformer.c]
Line 2: Crashing Input: [The exact raw text of the single log line that caused the crash, without the trailing newline]
Line 3: Preceding Output: [The expected JSON string output for the log line immediately preceding the crashing line]

Example `/home/user/diagnostic_report.txt`:
Function: parse_data
Crashing Input: 2023-01-01 BADLOG No Delimiters
Preceding Output: {"timestamp":"2023-01-01", "level":"INFO", "message":"All good", "msg_len":8}