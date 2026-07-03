You are a support engineer troubleshooting an intermittent crash in a critical Python network service. The service occasionally dies without leaving a standard Python traceback, and we suspect it's being triggered by a specific anomalous network request.

We have captured the network traffic during the most recent crash window and saved it at `/home/user/traffic.pcap`. 

The service source code is located at `/home/user/server.py`. 

Your diagnostic tasks are to:
1. Analyze the packet capture (`/home/user/traffic.pcap`) to identify the anomalous payload that triggers the crash. Normal requests are always exactly 4 bytes long (e.g., "PING"). The anomalous payload has a different length and structure.
2. Identify the source IP address that sent this anomalous payload.
3. Determine the exact signal name that kills the process when this payload is received (e.g., SIGILL, SIGSEGV, SIGABRT). You may need to run the server locally under a tracing tool like `strace` or a debugger, and send the payload yourself to observe the crash.

Once you have identified these details, create a diagnostic report at `/home/user/diagnostic_report.json` with the following exact JSON structure:
```json
{
  "malicious_ip": "<source IP address>",
  "payload_hex": "<the anomalous payload represented as a lowercase hex string>",
  "fatal_signal": "<the name of the terminating signal, e.g., SIGSEGV>"
}
```

Ensure your final JSON file is strictly formatted and contains exactly these three keys.