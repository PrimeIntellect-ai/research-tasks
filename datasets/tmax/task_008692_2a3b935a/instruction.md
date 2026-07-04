You are an edge computing engineer responsible for deploying a new version of a connectivity monitoring agent to a fleet of simulated IoT devices running locally.

Your goal is to write the new monitoring agent in C, and create a robust bash deployment script that performs a staged rollout with automated rollback capabilities.

Here is the current state of the system:
- The base directory for edge nodes is `/home/user/edge_fleet/`.
- There are three nodes: `/home/user/edge_fleet/node_1/`, `/home/user/edge_fleet/node_2/`, and `/home/user/edge_fleet/node_3/`.
- Each node directory contains:
  - `config.txt`: Contains a single integer representing the local TCP port this node should monitor.
  - `versions/v1/`: Contains the previous (dummy) version of the software.
  - `current`: A symbolic link currently pointing to `/home/user/edge_fleet/node_X/versions/v1`.

You need to perform two main tasks:

**Part 1: The C Monitoring Agent**
Write a C program at `/home/user/workspace/monitor.c` that does the following:
1. Accepts exactly one command-line argument: the absolute path to the node's directory.
2. Reads the target port from `{node_directory}/config.txt`.
3. Performs a connectivity diagnostic by attempting to establish a TCP connection to `127.0.0.1` on that port.
4. Writes the result to `{node_directory}/status.log`. 
   - If the connection is successful, write exactly `STATUS: UP` to the file and exit with return code `0`.
   - If the connection fails (e.g., connection refused), write exactly `STATUS: DOWN` to the file and exit with return code `1`.

**Part 2: The Staged Deployment Script**
Write a bash script at `/home/user/workspace/deploy.sh` that automates the deployment:
1. Compiles `/home/user/workspace/monitor.c` into an executable named `monitor_v2`.
2. Iterates through all nodes in `/home/user/edge_fleet/` (`node_1`, `node_2`, `node_3`).
3. For each node, perform a staged deployment:
   a. Create a new directory: `{node_directory}/versions/v2/`.
   b. Copy the compiled `monitor_v2` executable into this new directory as `monitor`.
   c. Update the `{node_directory}/current` symlink to point to the new `versions/v2` directory.
   d. Execute the newly deployed monitor via the symlink: `{node_directory}/current/monitor {node_directory}`.
   e. Implement error handling based on the exit code of the monitor program:
      - If it exits with `0`, append a line to `/home/user/workspace/deploy.log` in the format: `[node_name]: SUCCESS`.
      - If it exits with `1` (or any non-zero), rollback the deployment by pointing the `{node_directory}/current` symlink back to `versions/v1`. Then append a line to `/home/user/workspace/deploy.log` in the format: `[node_name]: ROLLBACK`.

Once you have written both files, run your `/home/user/workspace/deploy.sh` script to execute the deployment.