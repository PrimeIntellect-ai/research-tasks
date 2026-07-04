You are an operations engineer triaging a production incident. Our custom logging daemon, `logd`, is experiencing two major issues:

1. **Freezes under load:** The service frequently hangs and stops processing new logs. Operations has noticed this usually happens right after a malformed or empty log message is sent to it.
2. **Format parsing edge-case:** Valid log messages that contain certain characters (specifically, messages that begin with a `[` character after the severity level, e.g., `[INFO] [System] started`) are being improperly parsed or rejected.

The source code for the daemon is located at `/home/user/log_service/logd.c`.
A Makefile and a test script are provided in the same directory.

Your task is to:
1. Debug and identify the root cause of the freezing/deadlock issue in `logd.c`.
2. Identify and fix the format parsing bug so that messages like `[INFO] [System] started` are parsed correctly, retaining the full message `[System] started`.
3. Modify `/home/user/log_service/logd.c` to fix both issues.
4. Ensure the program compiles successfully by running `make`.
5. Run `make test` to verify your fixes. 
6. Once the tests pass, create a file named `/home/user/fix_summary.txt` containing a brief, one-sentence explanation of what you changed to fix the deadlock, and a one-sentence explanation of how you fixed the parser.

You may use standard tools like `gdb`, `strace`, and any shell commands you need to debug the system.