You are acting as a backup operator testing a new automated restore validation system. Your task involves setting up a local git-based backup destination, implementing strict storage quotas using a custom C++ utility, and establishing a port-forwarding tunnel for monitoring.

Perform the following tasks:

1. **Storage Quota Enforcer (C++)**:
   Write a C++ program at `/home/user/quota_check.cpp` that calculates the total size (in bytes) of all files in a given directory recursively. 
   - The program must take exactly two command-line arguments: `<directory_path>` and `<max_bytes>`.
   - If the calculated size is strictly greater than `<max_bytes>`, the program must print `QUOTA EXCEEDED` to standard output and exit with status code `1`.
   - Otherwise, it must print `OK` to standard output and exit with status code `0`.
   - Compile this program to an executable at `/home/user/quota_check` using C++17 (`g++ -std=c++17`).

2. **Git Backup Server & Pre-receive Hook**:
   - Initialize a bare Git repository at `/home/user/restore_target.git`.
   - Create a `pre-receive` hook script in `/home/user/restore_target.git/hooks/pre-receive`.
   - This hook must execute your `/home/user/quota_check` utility, passing the repository directory (`/home/user/restore_target.git`) and a strict quota of `5000000` bytes (5 MB).
   - If the quota check fails (exit code 1), the hook must reject the push. Ensure the hook is executable.

3. **Monitoring Port Forwarding**:
   Our monitoring system expects to ingest logs on port 18080, but the internal ingestor runs on 19090. 
   - Use `socat` to create a TCP IPv4 port forwarder that listens on local port `18080` and forwards traffic to `127.0.0.1:19090`.
   - Run this `socat` process in the background.
   - Save the PID of the background `socat` process to exactly `/home/user/socat.pid`.

4. **Testing the Restore (Quota Breach)**:
   - Create a local git repository at `/home/user/backup_client`.
   - Generate a 6 MB dummy file named `payload.dat` in this repository (e.g., using `dd` from `/dev/urandom`).
   - Commit this file to the `master` branch.
   - Add `/home/user/restore_target.git` as a remote named `origin`.
   - Attempt to push the `master` branch to `origin`.
   - Redirect the combined standard output and standard error of the `git push` command to `/home/user/push_failed.log`. The push must fail because of your hook, and the log should capture the remote hook output containing `QUOTA EXCEEDED`.