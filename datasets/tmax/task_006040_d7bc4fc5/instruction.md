You are an engineer diagnosing why a custom Go-based user-level logging daemon is failing to start. The daemon is supposed to manage log configuration and rotation for local applications, but it immediately crashes upon startup due to a filesystem configuration error.

You have been provided with the crash output in a log file: `/home/user/logs/crash.log`. The source code for the daemon is located at `/home/user/app/main.go`.

Perform the following steps to diagnose and fix the issue:
1. Use text processing tools (e.g., `grep`, `awk`) to analyze `/home/user/logs/crash.log` and identify the restricted system file path the daemon is attempting to open (which causes the permission denied panic).
2. Use `sed` to modify `/home/user/app/main.go` in-place, replacing the restricted system file path with a local path: `/home/user/app/logs/app.log`.
3. Create any missing directories required by the new path so the filesystem is properly structured for the daemon.
4. Compile the fixed Go application to `/home/user/app/daemon` (e.g., using `go build -o /home/user/app/daemon /home/user/app/main.go`).
5. Run the newly compiled daemon. If the filesystem and configuration are correct, it will successfully perform its initial log rotation and print a startup message to standard output. 
6. Redirect this standard output to `/home/user/success.txt`.

Ensure your final state has the compiled binary, the correctly created log directory, and the `success.txt` file containing the daemon's startup message.