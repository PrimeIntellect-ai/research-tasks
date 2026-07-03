You are an edge computing engineer deploying a lightweight metrics aggregator to a fleet of IoT devices. You need to build a deployment automation script, write a Go-based metrics parser, and properly configure file permissions to ensure the security of the edge node.

Your objective is to complete the deployment pipeline by creating the necessary code, configuration, and automation scripts.

Here is the specification of what you need to build:

1. **Go Log Parser (`/home/user/edge_parser.go`)**:
   Write a Go program that calculates the average of temperature values.
   - It must read a JSON configuration file at `/home/user/config.json`. The JSON will have the following structure: `{"input_file": "<path>", "output_file": "<path>"}`.
   - It must open the file specified by `input_file`. This file will contain a list of integer temperature values, one per line.
   - It must calculate the average of these integers.
   - It must write the result to the file specified by `output_file` in the exact format: `Average_Temp: <value>` (formatted to exactly 2 decimal places, e.g., `Average_Temp: 92.00`).

2. **Automation & Text Processing Script (`/home/user/deploy.sh`)**:
   Write a bash script that handles the end-to-end data processing and deployment. When executed, this script must perform the following actions in order:
   - Parse the raw system log file located at `/home/user/raw_sensors.log`. Use standard text processing tools (`grep`, `awk`, `sed`, etc.) to extract *only* the numeric temperature values (ignoring the 'C' suffix) from lines that contain the word `CRITICAL`.
   - Save these extracted numeric values, one per line, into `/home/user/filtered_logs.txt`.
   - Programmatically create the configuration file `/home/user/config.json` with `input_file` pointing to `/home/user/filtered_logs.txt` and `output_file` pointing to `/home/user/metrics.out`.
   - Compile your Go program `edge_parser.go` into an executable named `/home/user/edge_bin`.
   - Secure the binary by setting its permissions to strictly `0500` (read and execute for the owner only, no permissions for group/others).
   - Execute the compiled `/home/user/edge_bin`.
   - Secure the resulting output metrics file by setting the permissions of `/home/user/metrics.out` to strictly `0400` (read-only for the owner, no permissions for group/others).

**Environment Assumptions**:
- Go is installed and available in the environment.
- `/home/user/raw_sensors.log` already exists (you do not need to create it, but you should inspect it or assume it looks like: `[2023-11-01 10:00] [CRITICAL] Sensor: 14 Temp: 95C Humidity: 80%`).

To complete the task, write the Go code and the Bash script as specified, and then execute your `deploy.sh` script so that all artifacts and final outputs are generated and properly secured.