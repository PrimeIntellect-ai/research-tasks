You are an infrastructure engineer automating a local provisioning pipeline. You have inherited a local CI logging tool written in C++ that has a severe bug: similar to an SSH configuration silently dropping valid keys, this tool silently drops critical log messages.

Your objective is to fix the pipeline, process the incoming build data, and properly configure log rotation.

**Initial State:**
* A raw CI output file exists at `/home/user/raw_build.txt`.
* A logging utility source file exists at `/home/user/ci_logger.cpp`. It reads from standard input and appends to `/home/user/logs/ci_build.log`.
* The `ci_logger.cpp` utility currently has a bug where it silently ignores and drops any line containing the word `FATAL`.

**Step 1: Fix and Compile the Logger**
Modify `/home/user/ci_logger.cpp` so that it correctly writes lines containing `FATAL` to the log file instead of skipping them.
Compile the fixed C++ code into an executable located at `/home/user/ci_logger`. (Use `g++` with standard settings).

**Step 2: Create a Robust CI Script**
Create a bash script at `/home/user/run_ci.sh` that performs the following text processing pipeline:
1. Enables robust error handling (e.g., fails on any error or pipeline failure).
2. Reads `/home/user/raw_build.txt`.
3. Filters the output to keep *only* lines that begin exactly with `[CI]`.
4. Replaces any occurrence of the exact word `ERROR` with the word `FATAL`.
5. Pipes the final processed output directly into `/home/user/ci_logger`.

Run your script `/home/user/run_ci.sh` once so that the data is processed and written to `/home/user/logs/ci_build.log`.

**Step 3: Configure Log Rotation**
Create a logrotate configuration file at `/home/user/logrotate.conf` specifically for the `/home/user/logs/ci_build.log` file. Apply the following rules:
* Rotate daily (`daily`)
* Keep 3 backups (`rotate 3`)
* Compress rotated files (`compress`)
* Do not fail if the log file is missing (`missingok`)

Finally, manually force a log rotation as a non-root user by running the logrotate utility. You must specify a user-writable state file so it does not attempt to use the system-wide state. Run exactly:
`logrotate -f -s /home/user/logrotate.status /home/user/logrotate.conf`

Ensure all output files remain in `/home/user/logs/` and the newly rotated file is properly compressed.