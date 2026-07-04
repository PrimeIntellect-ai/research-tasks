You are an expert systems programmer and backup administrator. You need to create a continuous data archiving daemon that parses legacy and incoming logs to extract critical backup failures.

Your objective is to write a C program and an accompanying text transformation script that fulfills the following requirements:

1. **Directories**: 
   - Legacy logs: `/home/user/legacy_logs/`
   - Incoming logs: `/home/user/incoming/`
   - Archive output: `/home/user/archive/`
   (You should create these directories if they don't exist).

2. **Text Transformation Script**:
   Create a bash script at `/home/user/filter.sh`. This script must take a single file path as an argument. Using `awk` or `sed`, it must extract only the lines containing the exact string `[CRITICAL]` from the file, and output them to `stdout`. Ensure the script is executable.

3. **C Archiver Daemon**:
   Write a C program at `/home/user/archiver.c` and compile it to `/home/user/archiver`.
   The program must perform the following actions in order:
   
   **Phase 1: Recursive Traversal**
   Recursively traverse the directory `/home/user/legacy_logs/` finding all files that end with `.log`.
   For each file found, invoke your `/home/user/filter.sh` script via `popen()` to extract the critical lines.
   Append all extracted critical lines to `/home/user/archive/master_critical.log`.
   
   **Phase 2: Atomic State Management**
   Maintain a running total of the *number of critical lines* extracted so far.
   Every time a file is processed (both legacy and incoming), update a summary file at `/home/user/archive/summary.json`.
   To prevent corruption during system crashes, this update **must be atomic**: write the JSON string `{"total_critical": X}` (where X is the integer count) to `/home/user/archive/summary.tmp`, then use the `rename()` system call to overwrite `/home/user/archive/summary.json`.

   **Phase 3: File Watching**
   After processing all legacy logs, use `inotify` to monitor the `/home/user/incoming/` directory for `IN_CLOSE_WRITE` events (new files finishing writing).
   When a new file triggers the event, check if it ends in `.log`. If it does, process it exactly like the legacy logs (extract lines via script, append to `master_critical.log`, and atomically update `summary.json`).

4. **Execution**:
   Compile your C program without warnings: `gcc -o /home/user/archiver /home/user/archiver.c`
   Start your daemon in the background: `/home/user/archiver &`
   Ensure it is running and has processed any files currently in the directories before you finish.

Note: I have already placed some test logs in `/home/user/legacy_logs/`. Once your program is running in the background, my automated test suite will drop a new log into `/home/user/incoming/` and verify that `master_critical.log` and `summary.json` update correctly within 2 seconds.