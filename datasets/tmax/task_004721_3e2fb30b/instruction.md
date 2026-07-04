You are an edge computing engineer deploying a new IoT sensor aggregation node. 

Your task consists of three main objectives: fixing a vendored monitoring agent, writing a setup script for data directories, and developing a C-based filter for incoming network payloads.

1. **Fix the Vendored Agent**
There is a vendored package located at `/app/sensor-agent-1.0.0` which contains the source code for our local system monitoring agent. Currently, it fails to compile due to a configuration issue. 
- Identify the compilation error and fix it (you can modify the files in `/app/sensor-agent-1.0.0`). 
- Compile the agent.
- Run the compiled `sensor-agent` in the background. It must remain running.

2. **Environment Setup Script**
Write an idempotent bash script at `/home/user/setup_env.sh` that does the following:
- Creates the directory `/home/user/sensor_data` if it doesn't exist.
- Sets the base permissions of `/home/user/sensor_data` to `750` (`rwxr-x---`).
- Uses Access Control Lists (ACLs) to grant the `nobody` user read and execute access (`r-x`) to this directory. Ensure this script is idempotent (running it multiple times should result in the same state without errors).
- Records the PID of the running `sensor-agent` process into `/home/user/sensor.pid`.

3. **Payload Filter (C Programming)**
IoT devices will send metric payloads over the network, but we need to sanitize them before writing them to the data directory. 
Write a C program at `/home/user/filter.c` and compile it to `/home/user/filter`.
- The program must read lines from `stdin` until EOF.
- For each line read, check if it contains any of the following restricted shell metacharacters or path traversal sequences: `;`, `&`, `|`, `$`, or the exact substring `../`.
- If a line contains ANY of those restricted patterns, the program MUST completely discard the line.
- If a line is clean (contains none of the restricted patterns), the program MUST print the line to `stdout` exactly as it was received (including the newline character).
- Ensure your C program does not truncate long lines arbitrarily (handle lines up to at least 2048 characters).

You must leave the compiled executable exactly at `/home/user/filter` and the running agent's PID in `/home/user/sensor.pid`.