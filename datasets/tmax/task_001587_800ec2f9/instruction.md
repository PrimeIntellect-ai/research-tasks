You are a monitoring specialist tasked with setting up a custom alert system for a staged deployment environment. Our application communicates via Unix domain sockets, but during recent rolling deployments, misconfigurations have occurred—specifically, regular files being created instead of sockets (similar to a 502 bad gateway caused by a wrong upstream path), or locale/timezone regressions.

Your task is to write a C++ program that monitors the current staged deployment, detects anomalies, triggers a backup of the corrupted deployment, and logs an alert.

**Environment details:**
*   Deployment directory: `/home/user/deploy/`
*   Inside this directory, there are multiple versioned folders (e.g., `v1`, `v2`, `v3`) and a symlink named `current` pointing to the active deployment.
*   Backup directory: `/home/user/backups/` (you must create this directory).
*   Workspace: `/home/user/monitor/` (write your code here).

**C++ Monitor Requirements:**
Write a C++ program `/home/user/monitor/monitor.cpp` and compile it to `/home/user/monitor/check_deploy`.
The program should take one argument: the path to the active deployment (which will be `/home/user/deploy/current`).
When executed, it must perform the following checks on the target directory:

1.  **Socket Check:** Verify that a file named `app.sock` exists inside the active deployment directory and that it is genuinely a Unix Domain Socket (not a regular file or directory).
2.  **Locale/Timezone Check:** Read the `config.meta` file inside the deployment directory. It contains key-value pairs. Verify that `TZ` is strictly `UTC` and `LANG` is strictly `en_US.UTF-8`.

**Anomaly Handling:**
If any check fails:
1.  **Alert Logging:** Append a line to `/home/user/monitor/alerts.log` strictly in this format:
    `ALERT: Target <real_target_dir_name> failed. Reason: <SocketError|ConfigError>`
    *(Note: `<real_target_dir_name>` should be the resolved name of the directory the symlink points to, e.g., `v2`. Use `SocketError` if the socket is missing or not a socket file. Use `ConfigError` if the config file is missing or has incorrect TZ/LANG.)*
2.  **Backup:** Execute a system command from within the C++ program to create a gzip-compressed tar archive of the failed deployment directory. The archive must be saved as `/home/user/backups/failed_<real_target_dir_name>.tar.gz`.

If no anomaly is found, output `OK` to standard output and exit gracefully.

**Execution Steps for You:**
1.  Create `/home/user/backups/`.
2.  Write and compile `monitor.cpp` using `g++ -std=c++17`.
3.  Run `./check_deploy /home/user/deploy/current`
4.  Update the `/home/user/deploy/current` symlink to point to `/home/user/deploy/v3` and run `./check_deploy /home/user/deploy/current` again.
5.  Update the symlink to point to `/home/user/deploy/v1` and run the tool one last time.

Ensure your code handles symlink resolution properly to extract the real directory name (`v1`, `v2`, etc.) for the logs and backups.