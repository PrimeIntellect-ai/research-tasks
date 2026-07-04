You are a Linux systems engineer hardening a server configuration. You have a scheduled monitoring script that is supposed to check disk usage and trigger an email alert via a helper script. However, it currently fails when run in restricted environments (like cron) due to missing environment variables, path issues, and missing pre-flight connectivity checks.

Your task is to fix the shell script and the Rust monitoring program so they work together robustly.

Here is the current system state and what you need to achieve:

1. **The Target Data:**
   There is a directory at `/home/user/data` that contains several files. 

2. **The Alert Helper:**
   There is an existing helper script at `/home/user/bin/send_alert.sh`. When executed, it reads the `ALERT_DIR` environment variable and writes an alert message to `$ALERT_DIR/email.txt`.

3. **The Shell Wrapper (`/home/user/run_monitor.sh`):**
   This script is executed by a scheduler, which provides a very minimal environment. You must edit `/home/user/run_monitor.sh` to:
   * Be idempotent: create the directory `/home/user/alerts` if it does not already exist.
   * Export the `ALERT_DIR` environment variable set to `/home/user/alerts`.
   * Safely append `/home/user/bin` to the `PATH` environment variable so the helper script can be found without an absolute path.
   * Perform a connectivity diagnostic: Check if the local mail relay is reachable on `127.0.0.1` port `2525`. You can use `nc -z 127.0.0.1 2525`. 
     * If it is NOT reachable, write exactly `Mail offline` to `/home/user/monitor_status.log` and exit with status `1`.
     * If it IS reachable, proceed to run the Rust monitor binary located at `/home/user/disk_monitor`. Write `Success` to `/home/user/monitor_status.log` upon completion.

4. **The Rust Monitor (`/home/user/main.rs`):**
   A junior engineer wrote a draft Rust program at `/home/user/main.rs`. You must fix and compile it.
   * The program needs to calculate the total size (in bytes) of all files directly inside `/home/user/data`. (You can assume no subdirectories).
   * If the total size exceeds `50000000` bytes (50 MB), the Rust program must execute the command `send_alert.sh` (relying on the PATH set by the wrapper script).
   * Compile your fixed code using `rustc /home/user/main.rs -o /home/user/disk_monitor`.

Once you have fixed `/home/user/run_monitor.sh` and compiled `/home/user/disk_monitor`, verify your setup by ensuring a background listener is on port 2525 (e.g., `python3 -m http.server 2525 &`) and then executing `bash /home/user/run_monitor.sh`. 

The automated test will verify the existence and contents of `/home/user/alerts/email.txt` and `/home/user/monitor_status.log`.