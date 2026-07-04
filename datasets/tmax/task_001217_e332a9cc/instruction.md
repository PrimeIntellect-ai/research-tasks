You are acting as a FinOps analyst tasked with optimizing cloud infrastructure costs. We have an environment with several running containers, and we need to automatically identify and "stop" idle containers to save money.

Your task is to implement a robust automation pipeline using C++ and Bash.

1. **Create a C++ program** at `/home/user/analyzer.cpp` that reads a CSV file of container metrics.
   - The program should accept the CSV file path as its first command-line argument.
   - The CSV file has no header. Each line is formatted as: `ContainerID,CPU_Usage,Memory_Usage` (where CPU and Memory are floats).
   - A container is considered "idle" if its `CPU_Usage` is strictly less than 5.0 AND its `Memory_Usage` is strictly less than 50.0.
   - The program must print only the `ContainerID` of every idle container to standard output (one ID per line).

2. **Create a shell script** at `/home/user/optimizer.sh` that acts as the automation wrapper. The script must:
   - Check if the file `/home/user/metrics.csv` exists. If it does not exist, the script must exit immediately with status code 1.
   - Compile `/home/user/analyzer.cpp` using `g++` into an executable named `/home/user/analyzer`.
   - Execute `/home/user/analyzer` passing `/home/user/metrics.csv` as the argument.
   - For every container ID outputted by the C++ program, append the exact line `STOPPED: <ContainerID>` to the log file `/home/user/stopped_containers.log` (this simulates the container lifecycle management action).

3. **Configure scheduling:**
   - Create a crontab file at `/home/user/finops.cron` that schedules `/home/user/optimizer.sh` to run every day at exactly 2:00 AM. 

Make sure `/home/user/optimizer.sh` is executable. You do not need to start the cron daemon; just create the configuration file. Do not use absolute paths for system commands like `g++` or `bash` assuming specific bin locations, but strictly use `/home/user/...` for all the files you create or reference.