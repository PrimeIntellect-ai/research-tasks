You are a capacity planner building a custom resource monitoring and process supervision tool to analyze application memory leaks and behavior under stress.

Your objective is to build a complete suite that includes a simulated memory-leaking worker, a Go-based supervisor daemon, and an analysis script.

Perform the following steps:

1. Create a simulated worker script at `/home/user/dummy_worker.sh`
This must be an executable bash script that intentionally leaks memory over time. It should run an infinite loop where it sleeps for 0.1 seconds and appends a large chunk of random text (e.g., 5000 characters from `/dev/urandom`) to a variable in memory.

2. Create a Go-based supervisor daemon at `/home/user/monitor.go`
Write a Go program that does the following:
- Spawns `/home/user/dummy_worker.sh` as a child process.
- Runs a monitoring loop every 100 milliseconds.
- In each iteration, determines the Resident Set Size (RSS) memory of the child process in KB (you may use `ps -o rss= -p <PID>`).
- Appends the telemetry data to `/home/user/metrics.log` in the exact format: `<UnixTimestamp>,<PID>,<RSS_KB>`
- Implement Log Rotation: Before writing, check the size of `/home/user/metrics.log`. If it is strictly greater than 5000 bytes, rename it to `/home/user/metrics.log.1` (overwriting the old backup if it exists) and start a new `/home/user/metrics.log`.
- Implement Health Checks & Restart Policy: If the child's RSS exceeds 15000 KB (15 MB), immediately kill the child process (using SIGKILL or equivalent), append a log entry to `/home/user/restarts.log` in the exact format `<UnixTimestamp>,RESTART`, and spawn a new instance of `/home/user/dummy_worker.sh` to continue monitoring.

3. Compile and Run
Compile the Go program to `/home/user/monitor`.
Run the compiled `/home/user/monitor` in the background for exactly 10 seconds, then gracefully or forcefully terminate it. Ensure that the child worker process is also terminated.

4. Create an Analysis Script at `/home/user/analyze.sh`
Write a shell script using `awk` (and any other standard text processing tools) that analyzes the generated logs. It must read all available metrics logs (`/home/user/metrics.log` and `/home/user/metrics.log.1` if it exists) and `/home/user/restarts.log`.
The script should output a summary report to `/home/user/report.txt` containing exactly two lines:
Line 1: `Max RSS: <value> KB` (where <value> is the maximum RSS_KB observed across all log entries)
Line 2: `Restarts: <count>` (where <count> is the total number of RESTART events found in restarts.log, or 0 if none)

Ensure all scripts are executable. Your analysis script should successfully execute and generate the `report.txt` file based on the 10-second run.