You are an IT support technician responding to an urgent escalation ticket regarding a legacy service called `bash-metrics-daemon`.

**Ticket Details:**
"Our legacy Bash-based metrics aggregator is crashing, and its calculations are severely rounded off. It's supposed to compute moving averages of system metrics, but it is returning integers instead of precise floating-point values. Worse, it crashed completely last night. We managed to capture the network traffic during the crash, which is saved at `/home/user/ticket/crash.pcap`.

Your tasks:
1. **Pcap Analysis & Fuzzing:** Inspect `/home/user/ticket/crash.pcap` using `tcpdump` to find the exact TCP payload that caused the daemon to crash. Then, write a quick fuzzing loop if needed to understand why the daemon's input parser dies when receiving that payload.
2. **Floating-Point Precision Repair:** The daemon computes averages using `bc`, but it's losing precision. Fix the daemon's script so that it outputs floating-point values rounded to exactly 4 decimal places (e.g., `AVG: 20.3333`).
3. **Fix the Crash:** Patch the daemon's code so that instead of crashing and exiting when it receives the malicious/malformed payload (or any non-numeric payload that breaks `bc`), it simply replies with `ERROR: BAD INPUT\n`.
4. **Deployment:** The daemon source is vendored at `/app/bash-metrics-daemon-1.0`. Once fixed, start the daemon so it listens persistently in the background on `127.0.0.1:9090`.

**Protocol Documentation:**
- The daemon uses a raw TCP protocol.
- Clients first send an authentication string: `AUTH x-daemon-token-99\n`. The server responds with `OK\n`.
- Clients then send metric payloads like: `METRIC CPU 15.5 20.0 30.2\n`.
- The server responds with the average: `AVG: 21.9000\n`.

Please analyze the pcap, repair the code in `/app/bash-metrics-daemon-1.0/server.sh`, and leave the patched service running on `127.0.0.1:9090` so our monitoring systems can connect to it.