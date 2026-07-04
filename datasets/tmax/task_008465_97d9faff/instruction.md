You are an edge computing engineer deploying a telemetry microservice stack to IoT devices. These devices have highly constrained storage, and a previous deployment failed because services couldn't communicate and logs filled up the disk.

Your goal is to fix the existing code, implement an idempotent setup script, create a Go-based storage monitor, and write a log analysis pipeline.

All your work should be done in the `/home/user/edge` directory.

**1. Network Misconfiguration**
Two Go microservices already exist in `/home/user/edge/`:
- `sensor.go`: Generates telemetry data and sends it via UDP.
- `collector.go`: Listens for UDP telemetry data and writes it to disk.
Currently, they cannot communicate due to a port mismatch. Inspect both files and patch `sensor.go` so it sends data to the port that `collector.go` is actively listening on.

**2. Idempotent Setup Script**
Write a shell script at `/home/user/edge/init.sh`. This script must be fully idempotent (safe to run multiple times without failure or unwanted side effects) and perform the following:
- Create the directory `/home/user/edge/bin/`.
- Compile `sensor.go` into an executable at `/home/user/edge/bin/sensor`.
- Compile `collector.go` into an executable at `/home/user/edge/bin/collector`.
Make sure `init.sh` is executable.

**3. Storage Quota Enforcement (Go)**
Because edge devices have limited disk space, write a Go program at `/home/user/edge/quota.go` and compile it to `/home/user/edge/bin/quota`.
This program must:
- Accept two command-line arguments: a directory path and a maximum size limit in bytes (e.g., `./quota /home/user/edge/logs 1048576`).
- Calculate the total size of all `.log` files in the given directory.
- If the total size exceeds the specified limit, it must delete the **oldest** `.log` file (based on file modification time).
- It should repeat this deletion process until the total size of `.log` files is strictly less than or equal to the size limit.

**4. Log Processing Pipeline**
The logs in `/home/user/edge/logs/` contain standard telemetry and error messages.
Write a shell script at `/home/user/edge/process.sh` (make it executable) that uses text processing tools (`awk`, `grep`, `sed`, etc.) to parse all `.log` files in the logs directory.
It should find all lines containing the string `[ERROR]` and extract the numeric error code. The log lines look like this:
`2023-10-12T08:00:00Z [ERROR] Code 502: Bad Gateway`
The script must count the occurrences of each error code across all log files and output the summary to `/home/user/edge/error_summary.txt`.
The format of `error_summary.txt` must be exactly:
```
<ErrorCode>: <Count>
```
For example:
```
404: 12
502: 3
```
Sort the output numerically by the error code in ascending order.

To complete the task, ensure `sensor.go` is patched, all scripts and binaries are created in their specified locations, and then run `./init.sh`, run `./bin/quota /home/user/edge/logs 500000`, and run `./process.sh`.