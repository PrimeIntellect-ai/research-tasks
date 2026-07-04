You are a Site Reliability Engineer (SRE) investigating intermittent failures in an uptime monitoring script. 

You have been provided with:
1. `/home/user/monitor.sh`: A Bash script that takes a base64-encoded payload as its first argument, decodes it, and checks if the service status is "UP".
2. `/home/user/uptime_traffic.pcap`: A recent network packet capture containing traffic from the monitored service.

Recently, the cron job running `monitor.sh` has been failing with Bash syntax errors depending on the payload it receives.

Your tasks are:
1. **Network Analysis**: Inspect `/home/user/uptime_traffic.pcap` to understand the payloads being returned by the service. One of the payloads in this capture is responsible for crashing the monitoring script.
2. **Troubleshoot & Identify**: Determine exactly which decoded payload from the pcap file causes `monitor.sh` to throw a Bash syntax error. Write the exact decoded string (including any spaces or newlines) into `/home/user/crash_payload.txt`.
3. **Fuzz Testing**: Write a fuzzing script at `/home/user/fuzzer.sh` that calls `./monitor.sh` with at least 10 different randomly generated or edge-case base64 payloads. Your fuzzer should demonstrate that bad inputs can crash the original script.
4. **Fix the Script**: Modify `/home/user/monitor.sh` so that it safely handles *any* decoded payload without throwing Bash syntax errors (such as `too many arguments` or `unary operator expected`). The script should simply output "Service is DOWN" for any payload that isn't exactly "UP".

Ensure that `monitor.sh` and `fuzzer.sh` are executable. The success of this task will be verified by running your modified `monitor.sh` against malicious payloads and checking the contents of `crash_payload.txt`.