You are a DevOps engineer investigating a crashing legacy network service. You have been provided with logs, a network traffic dump, and the compiled service binary. The original C++ source code is lost.

Your goal is to identify the root cause of the anomalous behavior and generate a final debug report.

Here are the files you have in `/home/user`:
1. `/home/user/daemon_logs.txt`: Contains connection logs with latency metrics.
2. `/home/user/traffic_dump.txt`: A text-based hex dump of the recent network traffic captured on the server.
3. `/home/user/network_daemon`: The stripped C++ compiled binary of the service.

Perform the following steps using standard Linux terminal tools:
1. **Statistical Anomaly Investigation**: Parse `/home/user/daemon_logs.txt` to identify the single IP address that consistently causes a latency of over 500ms.
2. **Network Traffic Analysis**: Search through `/home/user/traffic_dump.txt` to find the network payload sent by this anomalous IP address. The payload is a single string starting with `CMD_`.
3. **Binary Reverse Engineering**: Examine the `/home/user/network_daemon` binary. The developer embedded a hidden C++ function to handle this specific command. The function's name includes the payload string (in lowercase). Find the exact *mangled* C++ symbol name for this function.

Finally, construct a regression debug report. Create a file at `/home/user/debug_report.txt` with exactly the following format:
```
IP: <Anomalous_IP>
PAYLOAD: <Payload_String>
FUNCTION: <Mangled_Function_Name>
```

Ensure your tools and commands are limited to bash built-ins and standard CLI utilities (`grep`, `awk`, `strings`, `nm`, `objdump`, etc.).