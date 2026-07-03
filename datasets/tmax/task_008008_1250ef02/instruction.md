You are an engineer diagnosing why a custom user-space daemon is failing to start and process its configuration properly. 

The daemon consists of a C++ application and a bash-based service management script that acts like a simplified init system. Currently, the service crashes or produces incorrect output because it mishandles filesystem paths, environment variables, and timezone configurations.

Your task is to fix the C++ source code, fix the service manager script, compile the application, and successfully start the daemon.

Here is the current system layout:
- `/home/user/src/daemon.cpp`: The source code for the daemon. It is incomplete/buggy.
- `/home/user/bin/service_manager.sh`: The init script intended to start, stop, and manage the lifecycle of the daemon.
- `/home/user/config/daemon.conf`: The configuration file containing the target epoch time to process.
- `/home/user/config/daemon.env`: Environment file containing variables (like `TZ`) that the daemon relies on.
- `/home/user/run/`: Directory where the daemon's PID file should be written.
- `/home/user/logs/`: Directory where the daemon's output should be written.

### Your Objectives:

1. **Fix the C++ Application (`/home/user/src/daemon.cpp`)**
   - The application must read the configuration file located exactly at `/home/user/config/daemon.conf`.
   - The config file contains a single line with an epoch timestamp: `TARGET_TIME=1700000000`. Parse this integer value.
   - The application must format this epoch time into a string with the exact format `%Y-%m-%d %H:%M:%S`. It must rely on the environment's `TZ` variable to determine the local time.
   - The formatted time must be written to `/home/user/logs/daemon_output.log`.
   - The application must also write its own PID (Process ID) to `/home/user/run/daemon.pid` upon starting, and keep running in an infinite sleep loop (e.g., `sleep(3600)`) until terminated.

2. **Fix the Service Manager Script (`/home/user/bin/service_manager.sh`)**
   - The script accepts one argument: `start` or `stop`.
   - On `start`: It must source `/home/user/config/daemon.env`, export the variables, and start the compiled daemon in the background (`&`).
   - On `stop`: It must read the PID from `/home/user/run/daemon.pid`, kill that process, and remove the PID file.

3. **Compilation and Execution**
   - Compile the C++ program to `/home/user/bin/daemon` (e.g., using `g++ -std=c++17 /home/user/src/daemon.cpp -o /home/user/bin/daemon`).
   - Start the service by running `/home/user/bin/service_manager.sh start`.

Leave the service running in the background. The automated test will verify that the daemon process is running, the PID file is correct, and `/home/user/logs/daemon_output.log` contains the correct timestamp formatted according to the configured timezone.