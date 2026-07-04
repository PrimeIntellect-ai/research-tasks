You are tasked with setting up a custom capacity monitoring system for a virtual storage cluster. As a capacity planner, you need to monitor logical storage usage, but with a specific caveat: some storage nodes are marked as offline and must be silently ignored, much like how a misconfigured SSH server might silently reject key-based logins without explicit errors.

Please complete the following steps using strictly Bash and standard Linux utilities:

1. **Logical Directory Management:**
   A raw storage backend exists at `/home/user/raw_storage/` containing subdirectories `node_alpha`, `node_beta`, `node_gamma`, and `node_delta`.
   Create a logical cluster structure at `/home/user/logical_cluster/`. 
   Inside `/home/user/logical_cluster/`, create symlinks named `vol1`, `vol2`, `vol3`, and `vol4` pointing to `node_alpha`, `node_beta`, `node_gamma`, and `node_delta` respectively.

2. **System Configuration:**
   Create a configuration file at `/home/user/capacity.conf`. It must contain exactly these two lines:
   ```
   THRESHOLD_BYTES=15000000
   ALERT_LOG=/home/user/capacity_alerts.log
   ```

3. **Capacity Daemon (Bash):**
   Write a Bash script at `/home/user/capacity-daemon.sh` that acts as a background monitoring daemon.
   - It should run in an infinite loop, pausing for 1 second (`sleep 1`) between iterations.
   - On each iteration, it must calculate the total size (in bytes) of all files in `/home/user/logical_cluster/` by following the symlinks.
   - **Crucial Rule:** If a target node directory contains a file named `.offline`, the daemon must *silently ignore* that entire volume in its total size calculation. Do not log an error for offline nodes.
   - If the calculated total active size is strictly greater than `THRESHOLD_BYTES` (read from the config file), it should append exactly this line to the `ALERT_LOG`:
     `CRITICAL: Usage at <TOTAL_BYTES> bytes` (replace `<TOTAL_BYTES>` with the actual calculated active byte count).
   - Ensure the script is executable.

4. **Service Lifecycle Management:**
   Since you do not have root access or systemd, write a SysV-style init script at `/home/user/cluster-init.sh` to manage your daemon.
   - It must accept one argument: `start` or `stop`.
   - `start`: Launches `/home/user/capacity-daemon.sh` in the background, redirects its stdout/stderr to `/dev/null`, and writes its Process ID to `/home/user/daemon.pid`.
   - `stop`: Reads the PID from `/home/user/daemon.pid`, gracefully terminates the process using `kill`, and removes the PID file.
   - Ensure the script is executable.

5. **Final Execution:**
   Start your service by running `/home/user/cluster-init.sh start`. Ensure it is running and has had a chance to write to the log (if the threshold is exceeded).