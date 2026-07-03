You are an observability engineer tuning custom dashboards for a legacy system. We need to extract specific CPU metrics from a worker process and format them for a Prometheus dashboard. 

Your task is to write a C++ utility to parse process metrics and a shell script to manage the process lifecycle and generate the final metrics file.

Step 1: Write a C++ program at `/home/user/extract_metrics.cpp`
This program must accept exactly one command-line argument: a Process ID (PID).
It should open and read `/proc/<PID>/stat`.
It needs to extract the 14th field (utime) and the 15th field (stime). (Note: fields in `/proc/[pid]/stat` are space-separated, and the 1st field is the PID).
The program must print exactly two lines to standard output in the following format:
`worker_cpu_utime{pid="<PID>"} <utime>`
`worker_cpu_stime{pid="<PID>"} <stime>`
If the file cannot be opened, the program should exit with a non-zero status.

Step 2: Compile the program
Compile your C++ program to the executable path: `/home/user/extract_metrics` (use standard `g++`).

Step 3: Write a shell script at `/home/user/run_observability.sh`
This script must perform the following actions in order:
1. Start the provided dummy worker script `/home/user/worker.sh` in the background.
2. Capture the PID of this background worker process.
3. Wait for exactly 2 seconds (to allow the worker to accumulate some CPU time).
4. Execute your compiled `/home/user/extract_metrics` program, passing the captured PID as the argument.
5. Redirect the standard output of the C++ program to `/home/user/node_metrics.prom`.
6. Terminate (kill) the background worker process gracefully.
7. Exit with status 0.

Ensure your shell script has executable permissions. When you are done, run your shell script once so that `/home/user/node_metrics.prom` is generated.