You are a monitoring specialist tasked with setting up a custom network alerting system. You need to write a C-based port checker, an alert dispatcher shell script, and a custom init script to manage the lifecycle of the monitoring daemon.

Your system must run entirely within `/home/user/netmon/`.
You do not have root privileges.

Follow these instructions to build the end-to-end scenario:

**Phase 1: Validation List**
There is a file called `/home/user/netmon/valid_users.txt` that contains a list of active system users (one per line).
There is also a configuration file at `/home/user/netmon/services.conf` with the format `port:owner_name` on each line.

**Phase 2: Alert Dispatcher Script**
Create a Bash script at `/home/user/netmon/trigger_alert.sh` that takes exactly two arguments: `owner_name` and `port`.
1. It must first check if the provided `owner_name` exists in `/home/user/netmon/valid_users.txt`.
2. If the user does not exist in the file, the script should exit immediately without doing anything.
3. If the user does exist, it must append the exact string: `ALERT: Service for [owner_name] on port [port] is unreachable!` to `/home/user/netmon/alerts.log`.
Make sure this script is executable.

**Phase 3: C-Based Network Checker**
Write a C program at `/home/user/netmon/check_ports.c` and compile it to `/home/user/netmon/check_ports` (using `gcc`).
1. The program must read `/home/user/netmon/services.conf`.
2. For each `port:owner_name` line, it must attempt to establish a TCP connection to `127.0.0.1` on that `port`.
3. If the connection fails (e.g., connection refused), the C program must execute your `/home/user/netmon/trigger_alert.sh` script, passing the `owner_name` and `port` as arguments. (You can use `system()` or `fork/exec` for this).
4. If the connection succeeds, it should gracefully close the socket and do nothing.
5. The program should exit after checking all entries in the file once.

**Phase 4: Service Lifecycle Management**
Create an init-style bash script at `/home/user/netmon/netmon-init.sh` that manages the execution of your checker. It must accept one argument: `start`, `stop`, or `status`.
- `start`: Starts a background process that runs `/home/user/netmon/check_ports` once, sleeps for 1 second, and repeats indefinitely. It must save the background process's PID to `/home/user/netmon/netmon.pid`.
- `stop`: Reads the PID from `/home/user/netmon/netmon.pid`, kills the background process, and removes the PID file.
- Make sure the script is executable.

Use your `netmon-init.sh` script to `start` the service. Let it run for at least 3 seconds, then use it to `stop` the service. Ensure `/home/user/netmon/alerts.log` is generated correctly.