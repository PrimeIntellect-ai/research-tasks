You are a security researcher analyzing a data exfiltration pipeline used by a suspicious binary. We have captured a large set of raw network payloads in `/app/data/raw_payloads.txt` (10,000 lines). 

We have reconstructed the malware's backend in a local multi-service environment under `/app/`. The environment consists of:
1. A Redis instance (listening on default port 6379).
2. A Flask-based C2 Server (`/app/c2_server.py`) listening on port 5000, which receives payloads and logs them to Redis.
3. A Bash-based Log Aggregator (`/app/aggregator.sh`) which simulates the malware by reading `raw_payloads.txt` line-by-line and sending them to the C2 server via curl.

**The Problem:**
When we run `/app/start_services.sh` and then execute `/app/aggregator.sh`, the aggregator eventually halts. There is a specific "poison pill" payload in `raw_payloads.txt` that triggers a crash (HTTP 500 / traceback) in the C2 Server, causing the aggregator script to abort before processing all lines.

**Your Objectives:**
1. **Error Diagnosis & Delta Debugging:** Analyze the crash. You must write a delta-debugging or bisection script (in any language, though bash/python are standard) to efficiently isolate the *exact single line* in the 10,000-line file that causes the C2 server to crash.
2. **Fix the Pipeline:** Once you identify the malicious payload, modify `/app/aggregator.sh` to detect and discard this specific payload line using intermediate assertion or validation, preventing it from being sent to the C2 server. 
3. **Integration & Execution:** Restart the C2 server if it died, and run your modified `/app/aggregator.sh` to completely process the `raw_payloads.txt` file.

**Verification:**
An automated test will verify your success using a numeric threshold metric. It will run a script to count the number of successfully stored payloads in the Redis database. To pass, the database must contain exactly the number of total lines minus the poison pill (e.g., 9,999 entries). You must leave the Redis server running with the final data loaded.