You are an engineer tasked with debugging a failing testing pipeline. 

In `/home/user/log_parser`, there is a C-based log parsing utility (`parser.c`) that extracts data from system logs. The build and test pipeline currently fails because the parser reliably segfaults when processing a recent log file (`logs.txt`). 

Your task is to investigate this failure, fix the code, and ensure it does not regress. 

Specifically, you must:
1. **Find the Anomaly**: The crash is caused by a single statistically anomalous log entry in `logs.txt` that triggers a format parsing edge-case. Identify the 1-indexed line number of this anomalous entry and write *only* this integer to `/home/user/log_parser/anomaly_line.txt`.
2. **Fix the Parser**: Modify `parser.c` to fix the buffer overflow. The program extracts usernames from lines formatted like `INFO User:<username> Action:<action>`. It uses a 32-byte buffer for the username. You must update the code to safely truncate usernames to a maximum of 31 characters (ensuring a null terminator fits) and prevent memory corruption. 
3. **Rebuild**: Recompile the binary to `/home/user/log_parser/parser` (a `Makefile` is provided).
4. **Create a Regression Test**: Write a Python script at `/home/user/log_parser/regression_test.py` that verifies the fix. The script should:
   - Generate a temporary test file containing a log line with a 100-character username.
   - Run the compiled `./parser` against this temporary file.
   - Exit with status code `0` if the parser runs successfully without crashing, and exit with status code `1` if the parser crashes or returns a non-zero exit code.

Ensure all outputs are placed exactly in the specified paths.