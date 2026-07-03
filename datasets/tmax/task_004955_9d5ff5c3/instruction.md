You are a Site Reliability Engineer (SRE) investigating an uptime monitoring system that has started failing. 

The system processes UDP heartbeat packets from edge nodes using a Python script located at `/home/user/uptime_monitor/process_heartbeats.py`. The heartbeat packets are captured in a pcap file at `/home/user/uptime_monitor/data/heartbeats.pcap`.

Recently, as edge nodes have been accumulating higher uptime values, the script has started failing intermittently, throwing a `ValueError` about "Negative timestamp detected" and crashing. The original developer suspected this was an issue similar to the classic x86 signed integer overflow, as the timestamp format appears to be misinterpreted when it exceeds a certain threshold.

Additionally, the script requires an HMAC secret key to verify the integrity of the packets via the `HEARTBEAT_SECRET` environment variable. The secret was originally hardcoded into the repository but was later removed and "secured". Unfortunately, the SRE team lost the documentation containing this key.

Your task:
1. Recover the missing HMAC secret key from the git repository's history in `/home/user/uptime_monitor`.
2. Debug and fix the `process_heartbeats.py` script so that it correctly parses the timestamps without treating large values as negative numbers.
3. Provide the secret key to the script (e.g., via environment variable) and run it against `data/heartbeats.pcap`.
4. The fixed script will output the maximum valid timestamp to `/home/user/uptime_monitor/max_timestamp.txt`.

Ensure your final fixed code runs successfully and writes the correct integer to `max_timestamp.txt`.