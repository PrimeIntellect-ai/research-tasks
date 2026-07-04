You are an engineer tasked with diagnosing and fixing a custom background data processor. The processor is supposed to read data files, transform them, and write outputs, but it is currently failing to run correctly due to environment path differences, a broken directory structure, and buggy C++ source code.

Because you do not have root access, the system uses a custom `~/pseudo_fstab` file to map real directories to application directories via symlinks. The application is managed by a user-space runner script that simulates a stripped-down environment (similar to cron).

Your tasks are:

1. **Link and Directory Management:**
   A mapping file exists at `/home/user/pseudo_fstab` with the format:
   `<real_target_directory> <symlink_path>`
   Write a shell command or script to parse this file and create the exact symlinks specified. Create any missing real target directories first. 

2. **Fix and Compile the C++ Daemon:**
   The source code for the daemon is located at `/home/user/src/processor.cpp`. 
   Currently, it attempts to write logs to a hardcoded path (`/var/log/processor.log`), which fails with permission denied. 
   Modify the C++ code to read the `LOG_DIR` environment variable instead, and write its log file to `$LOG_DIR/processor.log`. If `LOG_DIR` is not set, it should exit with code 1.
   Additionally, ensure it processes files from `$IN_DIR` and writes to `$OUT_DIR`. 
   Compile the fixed C++ code to `/home/user/app/bin/processor` (create the `bin` directory if needed).

3. **Configure the Service Manager:**
   The runner script `/home/user/service_manager.sh` launches the compiled processor. However, it clears all environment variables before running the daemon to simulate a strict scheduler environment.
   Modify `/home/user/service_manager.sh` so that it explicitly exports `LOG_DIR`, `IN_DIR`, and `OUT_DIR` pointing to `/home/user/app/logs`, `/home/user/app/input`, and `/home/user/app/output` respectively before executing `/home/user/app/bin/processor`.

4. **Log Analysis and Rotation Pipeline:**
   Create a shell script at `/home/user/rotate_and_report.sh` that:
   - Uses `grep` and `awk` to extract all lines containing the word "ERROR" from `/home/user/app/logs/processor.log`.
   - Writes these extracted lines to `/home/user/app/logs/error_summary.txt`.
   - Simulates log rotation by renaming `/home/user/app/logs/processor.log` to `/home/user/app/logs/processor.log.1`.

To verify your work:
- Run `/home/user/service_manager.sh`.
- Ensure it successfully processes the provided test file (`/home/user/real_data/input/data1.txt`).
- Execute your `/home/user/rotate_and_report.sh` script.

Leave the system in this final state.