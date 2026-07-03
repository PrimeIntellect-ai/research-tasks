You are a deployment engineer rolling out an update for a local filesystem data-processing daemon. The daemon is written in C++ and processes text files, but the latest rollout is crashing, and the monitoring pipeline needs to be established.

Your objectives:

1. **Fix the C++ Daemon:**
   The source code is located at `/home/user/deploy/src/processor.cpp`. It reads text files from `/home/user/deploy/data/in/`, processes them, writes to `/home/user/deploy/data/out/`, and logs heartbeats to `/home/user/deploy/logs/system.log`. 
   Currently, the daemon crashes entirely when it encounters a file containing the exact string "POISON_PILL". 
   Modify `/home/user/deploy/src/processor.cpp` so that instead of crashing, it gracefully skips the file, logs "WARNING: Poison pill skipped in <filename>" to the standard error, and continues running.
   Compile your fixed code to `/home/user/deploy/bin/processor` (use standard `g++ -std=c++17`).

2. **Implement a Health Monitor:**
   Write a bash script at `/home/user/deploy/scripts/monitor.sh` that acts as a basic container-like lifecycle manager for the daemon.
   - It should start the daemon `/home/user/deploy/bin/processor` in the background and record its PID to `/home/user/deploy/run/daemon.pid`.
   - It must run a continuous loop (checking every 2 seconds).
   - In each iteration, it should use `grep` or `awk` to check `/home/user/deploy/logs/system.log` for the "HEARTBEAT" keyword. If the daemon process has died (PID no longer exists) or if a heartbeat hasn't been logged in the last 5 seconds (simulated by checking if the daemon crashed), the monitor must automatically restart the daemon and update the PID file.
   - Run this monitor script in the background.

3. **Create a Log Analysis Pipeline:**
   Write a shell script at `/home/user/deploy/scripts/summary.sh` that uses text processing tools (`awk`, `sed`, `grep`) to parse `/home/user/deploy/logs/system.log` and outputs ONLY an integer representing the total number of successfully processed files (indicated by "SUCCESS: Processed <filename>" in the log).

Ensure all scripts are executable (`chmod +x`). Once you have completed the fixes, started the monitor, and the data in `/home/user/deploy/data/in/` has been processed, write the output of `/home/user/deploy/scripts/summary.sh` to a final verification file at `/home/user/deploy/summary_result.txt`.