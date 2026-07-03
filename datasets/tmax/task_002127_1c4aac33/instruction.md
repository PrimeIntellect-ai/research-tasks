You are acting as a Site Reliability Engineer managing a local configuration monitoring system.

We have a local Git repository at `/home/user/monitor_src` that tracks our monitoring scripts. Every time a commit is made, a Git `post-commit` hook is supposed to compile and run a C++ program (`monitor.cpp`) to log a status check.

However, the current setup has several issues similar to a classic cron PATH bug: the hook runs in varying environments, writes output to unpredictable relative paths, and logs in the wrong timezone. Furthermore, the C++ program is incomplete.

Your task is to fix the C++ program and the Git hook to meet the following specifications:

1. Modify `/home/user/monitor_src/monitor.cpp` so that it:
   - Takes exactly one command-line argument (`argv[1]`), which is the absolute path to the output log file.
   - Reads the system's `/etc/fstab` file.
   - Counts the number of active, valid mount entries (lines that are not empty and do not begin with `#`).
   - Retrieves the current system time.
   - Appends a single line to the file specified in `argv[1]` in the exact following format:
     `[YYYY-MM-DD HH:MM:SS UTC] FSTAB_ENTRIES: <count>`
     (e.g., `[2023-10-24 14:05:10 UTC] FSTAB_ENTRIES: 4`)

2. Modify the Git hook located at `/home/user/monitor_src/.git/hooks/post-commit` (a bash script) so that it:
   - Compiles `monitor.cpp` using `g++` into an executable named `monitor_run`.
   - Executes `monitor_run`, passing `/home/user/monitoring_logs/uptime.log` as the log file argument.
   - Explicitly enforces the `UTC` timezone for the C++ program execution by setting the `TZ` environment variable to `UTC` specifically for that run, ensuring the logged time is in UTC.

3. Trigger the hook by committing your changes to `monitor.cpp` in the `/home/user/monitor_src` repository.

Ensure the directory `/home/user/monitoring_logs/` exists before triggering the hook (create it if necessary). The automated test will read `/home/user/monitoring_logs/uptime.log` to verify correct execution, UTC timezone formatting, and accurate `/etc/fstab` parsing.