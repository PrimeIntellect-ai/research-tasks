You are acting as a capacity planner for a cluster, and you need to configure a local metrics analyzer daemon. The analyzer frequently crashes due to out-of-memory simulations and expects its upstream socket to be at a specific path, but the system's metrics collector writes to a different location. 

Your task is to create a supervision and configuration script that bridges these components and manages the analyzer's logs.

Specifically, write a bash script at `/home/user/planner/supervise.sh` that fulfills the following requirements:

1. **Directory Structure & Linking:**
   - Ensure the directories `/home/user/planner/run`, `/home/user/planner/logs`, and `/home/user/app` exist.
   - Create a symbolic link at `/home/user/planner/run/socket` that points to `/home/user/app/metrics.sock`. (The analyzer reads from the symlink, while the upstream daemon creates the actual socket).

2. **Log Rotation:**
   - The script must manage the analyzer's log file located at `/home/user/planner/logs/analyzer.log`.
   - Implement a simple rotation mechanism that keeps up to 3 historical logs (`analyzer.log.1`, `analyzer.log.2`, `analyzer.log.3`).
   - Every time the analyzer process is about to be started (or restarted), your script must rotate the existing logs: `analyzer.log.2` becomes `analyzer.log.3`, `analyzer.log.1` becomes `analyzer.log.2`, and `analyzer.log` becomes `analyzer.log.1`. (If a file doesn't exist, simply skip moving it).

3. **Process Supervision:**
   - After handling the rotation, the script must start the analyzer by running: `python3 /home/user/analyzer.py`
   - All standard output and standard error from the analyzer must be appended to `/home/user/planner/logs/analyzer.log`.
   - The analyzer is unstable and will exit periodically. Your script must run in an infinite loop, continuously rotating logs and restarting the analyzer whenever it exits.

Make sure your script is executable (`chmod +x`). Once you have created and verified the script, you are done. An automated test suite will execute `/home/user/planner/supervise.sh` in the background to verify the directory structure, symlink correctness, log rotation, and restart loop.