You are a monitoring specialist tasked with setting up an alerting pipeline for a secure filesystem drop-zone. You must build a custom C-based monitoring tool, configure permissions, prepare an SSH tunnel configuration for off-site reporting, and write a parsing pipeline.

Complete the following objectives:

1. **Directory Setup & ACLs:**
   Create a directory at `/home/user/secure_zone`. Use Access Control Lists (ACLs) to set the default mask for newly created files in this directory to read and execute only (no write permission for group/others).

2. **C-Based Filesystem Monitor:**
   Write a C program in `/home/user/fs_monitor.c` and compile it to `/home/user/fs_monitor`. 
   - The program must use `inotify` to monitor the `/home/user/secure_zone` directory specifically for `IN_CREATE` events.
   - For every new file created in the directory, the program must print a line to standard output in the exact format: `ALERT: New file <filename> detected` (where `<filename>` is just the name of the file, not the full path).
   - Ensure the program flushes standard output after each print so logs are not buffered.
   - Run this compiled program in the background and redirect its standard output to `/home/user/events.log`.

3. **Log Parsing Pipeline:**
   Write a shell script at `/home/user/process_alerts.sh` that reads `/home/user/events.log` and uses text processing tools (`grep`, `awk`, or `sed`) to extract just the filenames from the alert lines. The script must write only the filenames (one per line) to `/home/user/processed_files.txt`. Ensure the script has executable permissions.

4. **SSH Tunnel Configuration:**
   To prepare for forwarding these alerts to a central monitoring server, write a bash script at `/home/user/start_tunnel.sh` containing the exact `ssh` command to create a local port forward. The command should forward the local machine's port `8888` to `127.0.0.1:9999` on a remote server alias `monitor-server`. Run it in the background (`-f`, `-N`). You do not need to execute this script, just ensure the correct command is inside it and it is executable.

Ensure your C program is running in the background and logging to `/home/user/events.log` before you finish the task.