You are a DevOps engineer investigating an anomaly in your infrastructure's telemetry pipeline. The telemetry service normally calculates the average transaction latency from incoming network streams, but it is currently reporting truncated, inaccurate, and heavily rounded integer metrics.

Your investigation has narrowed the issue down to a specific environment and processing script. You need to debug and fix the pipeline to accurately calculate the average latency down to 4 decimal places.

Here is your environment:
1. `/home/user/telemetry.pcap`: A recent network packet capture containing the raw telemetry stream. The payloads are transmitted over UDP port 8080 and contain simple plaintext data in the format `LATENCY=<value>`.
2. `/home/user/process_telemetry.sh`: A Bash script designed to parse extracted logs and calculate the average latency. 

Your objectives are:
1. **Pcap Analysis**: Extract the raw ASCII payloads (specifically the `LATENCY=<value>` lines) from the UDP stream in `/home/user/telemetry.pcap` and save them to `/home/user/extracted_logs.txt`.
2. **Dependency & Environment Debugging**: The `process_telemetry.sh` script is mysteriously failing to use the correct system dependencies, causing some mathematical operations to misbehave entirely. Find the conflict in the environment or script configuration and resolve it so standard tools are used.
3. **Floating-Point Precision Repair**: Even with the correct tools, `process_telemetry.sh` loses floating-point precision when calculating the average. Fix the bash script so that all arithmetic operations retain precision, and the final average latency is calculated to exactly 4 decimal places.
4. **Execution**: Run the fixed `process_telemetry.sh` using `/home/user/extracted_logs.txt` as its input. Ensure the script writes its final output to `/home/user/final_report.txt` in the exact format: `Average Latency: <value>` (e.g., `Average Latency: 42.1234`).

Note: You may use standard CLI tools like `tshark`, `grep`, `awk`, `bc`, etc. Do not write a Python or Perl script to bypass `process_telemetry.sh`; you must fix the existing Bash script and its environment.