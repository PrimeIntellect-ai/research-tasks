You are a system administrator tasked with creating a custom bash-based watchdog daemon. Because you do not have root access, you need to build this using standard bash tools, managing the process lifecycle manually.

Please complete the following steps in the `/home/user` directory:

1. **Directory Structure:**
   Create the following directory structure:
   - `/home/user/watchdog/`
   - `/home/user/watchdog/links/`
   - `/home/user/watchdog/logs/`
   - `/home/user/watchdog/targets/`

2. **Watchdog Script (`/home/user/watchdog/daemon.sh`):**
   Write a bash script at `/home/user/watchdog/daemon.sh` (ensure it is executable). 
   The script must accept exactly one argument: `start` or `stop`.
   
   **When called with `start`:**
   - It should launch a background monitoring loop.
   - It must write the background process's PID to `/home/user/watchdog/daemon.pid`.
   - The script should exit, leaving the background loop running.

   **When called with `stop`:**
   - It should read the PID from `/home/user/watchdog/daemon.pid`.
   - Terminate the background process gracefully.
   - Remove the `daemon.pid` file.

   **Monitoring Loop Behavior:**
   - The loop should sleep for 1 second between iterations.
   - During each iteration, it should examine all symlinks in `/home/user/watchdog/links/`.
   - For each symlink:
     - If the symlink is broken (target does not exist), append exactly this string to `/home/user/watchdog/logs/watch.log`:
       `BROKEN: <symlink_basename>`
     - If the symlink is valid, check the octal permissions of its *target* file. If the permissions are not exactly `600`, append exactly this string to the log:
       `BADPERM: <symlink_basename> <actual_octal_permissions>` (e.g., `BADPERM: mylink 644`)
   - Ignore regular files or directories inside `links/`; only process symlinks.
   
   **Log Rotation:**
   - At the end of each iteration (after checking all links), check the size of `/home/user/watchdog/logs/watch.log`.
   - If the log file size is strictly greater than `100` bytes, rotate it by renaming it to `/home/user/watchdog/logs/watch.log.old`. (If `watch.log.old` already exists, overwrite it).
   - The next iteration should simply create a new `watch.log` when it needs to write.

Please implement the solution. Do not create any dummy targets or symlinks to test it; just write the script and prepare the directories. Do not start the daemon yourself; the automated testing suite will start it, inject test files, and evaluate your script's behavior.