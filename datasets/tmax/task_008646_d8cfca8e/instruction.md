You are acting as a DevOps engineer tasked with debugging a critical service that recently crashed. You have been provided with a dump of the container logs and the stack trace generated at the time of the crash.

Your goal is to investigate these files to find a statistical anomaly in the traffic just before the crash, and combine that with the stack trace to determine the root cause.

All necessary files are located in `/home/user/service_dump/`.
The directory contains two files:
1. `service.log`: The application container's access log leading up to the crash.
2. `crash_trace.txt`: The stack trace output from the application crash.

Your tasks:
1. **Log Inspection & Anomaly Investigation**: The service crashed at exactly `2023-10-27 10:15:00`. Look at the 5-minute window immediately preceding the crash (from `10:10:00` to `10:14:59` inclusive). Analyze the logs to find the IP address that generated a statistically anomalous number of `POST` requests to the `/api/upload` endpoint during this window compared to all other IPs.
2. **Stack Trace Analysis**: Inspect the `crash_trace.txt` file to identify the exact name of the C++ function that caused the `SIGSEGV` (Segmentation fault). The crashing function is the function at the top of the call stack (frame #0).

Once you have identified these details, create a report file at `/home/user/debug_report.json` with the following exact JSON structure:

```json
{
  "anomalous_ip": "IP_ADDRESS_HERE",
  "anomalous_request_count": 0,
  "crashing_function": "FUNCTION_NAME_HERE"
}
```

Replace `IP_ADDRESS_HERE`, `0` (with the integer count of requests from that IP to `/api/upload` during the 5-minute window), and `FUNCTION_NAME_HERE` with your findings. Do not include arguments or return types in the function name, just the bare function name (e.g., `process_payload`).