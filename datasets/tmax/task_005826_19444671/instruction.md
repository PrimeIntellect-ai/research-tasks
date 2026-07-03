You are a developer who recently inherited an unfamiliar codebase for a data processing pipeline. The system consists of a Node.js API gateway and a Python backend worker that communicate over a custom TCP protocol. 

Recently, the Python worker has been intermittently crashing in production. We managed to capture a packet trace (`traffic.pcap`) and some logs during the latest crash. 

Your task is to perform a forensic investigation and fix the issue:
1. Examine the provided files in `/home/user/app/`: `server.js` and `worker.py`.
2. Analyze `/home/user/data/traffic.pcap` to identify the network traffic that correlates with the crash. Reconstruct the timeline of events from `/home/user/logs/server.log` and `/home/user/logs/worker.log`.
3. You will discover a format parsing edge-case in `worker.py` that causes a fatal exception when processing a specific anomalous payload. Fix the bug in `/home/user/app/worker.py` so that it gracefully handles the parsing error (it should catch the exception, send back a `{"status": "error", "message": "Invalid payload format"}` response, and continue running without crashing).
4. Identify the source IP address that sent the anomalous payload through the API gateway (which was then forwarded to the worker).
5. Write the source IP address of the anomalous request to `/home/user/attacker_ip.txt`.

The custom protocol uses a 1-byte type, 4-byte length (big-endian), and a variable-length payload. The crash happens due to a specific decoding failure when the payload length is maliciously crafted, causing truncation during multi-byte character decoding.

Please ensure:
- `/home/user/app/worker.py` is patched.
- `/home/user/attacker_ip.txt` contains exactly the IPv4 address.