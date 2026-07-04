You are a monitoring specialist setting up a lightweight, custom process supervisor for a legacy service that has a habit of silently failing (it stops processing data and stops updating its heartbeat file, but the process doesn't die). 

Your task is to set up the directory structure, configuration, and a C++ supervisor program to detect this silent failure and simulate a restart.

Perform the following steps exactly as specified. All paths must be absolute, assuming your home directory is `/home/user`.

1. **Directory and Link Management:**
   - Create the following directories: `/home/user/config`, `/home/user/actual_configs`, `/home/user/run`, and `/home/user/logs`.
   - Create a configuration file at `/home/user/actual_configs/current.conf` containing exactly these two lines:
     ```
     HEARTBEAT_FILE=/home/user/run/hb.txt
     TIMEOUT=2
     ```
   - Create a symbolic link at `/home/user/config/service.conf` that points to `/home/user/actual_configs/current.conf`.

2. **Supervisor Construction (C++):**
   - Write a C++ program at `/home/user/supervisor.cpp` and compile it to the executable `/home/user/supervisor`.
   - The program must parse `/home/user/config/service.conf` to extract the `HEARTBEAT_FILE` path and the `TIMEOUT` value (as an integer).
   - The program must execute a supervision loop exactly 5 times. At the *beginning* of each loop iteration, it must sleep for exactly 1 second.
   - After the sleep in each iteration, it must check the last modified time (mtime) of the heartbeat file.
   - If `(current_system_time - mtime) > TIMEOUT`, the service is considered stalled. The supervisor must:
     a) Append the exact string `ALERT: Process stalled. Restarting.\n` to `/home/user/logs/alerts.log`.
     b) Simulate a process restart by updating the heartbeat file's modification time to the current time (equivalent to running the `touch` command on it).

3. **Execution and Testing:**
   - Initialize the simulated environment by creating an empty heartbeat file at `/home/user/run/hb.txt`.
   - Sleep for 3 seconds in your terminal.
   - Run your compiled `/home/user/supervisor` executable.

Ensure your C++ code correctly uses standard libraries for file I/O and time (e.g., `<sys/stat.h>`, `<unistd.h>`, `<utime.h>`, or C++17 `<filesystem>`). Leave the final generated `/home/user/logs/alerts.log` in place for verification.