You are acting as a security researcher analyzing a suspicious multi-service application found on a compromised Linux host. The malware consists of three cooperating services: an Nginx reverse proxy, a multi-threaded Python Flask backend, and a Redis instance used for caching intercepted payloads.

The startup script `/home/user/app/start.sh` launches all services, but the system is currently broken due to an environment misconfiguration, and even when fixed, the Flask backend deadlocks under high request contention. Furthermore, we discovered a corrupted SQLite database file at `/home/user/app/exfiltrated.db` which contains partial logs of the malware's custom payload format.

Your objectives are:
1. **Service Configuration & Debugging:** Fix the environment misconfiguration preventing Nginx from correctly routing traffic to the Flask app, and fix the Redis connection string in the Flask environment. 
2. **Concurrency Fix:** Analyze the Flask backend source code in `/home/user/app/backend/app.py`. There is a threading deadlock when processing concurrent requests to the `/process` endpoint. Fix the deadlock.
3. **Database Recovery & Formula Correction:** Recover the corrupted SQLite database (`/home/user/app/exfiltrated.db`) using its WAL/journal files. Within the recovered `payload_rules` table, you will find the correct mathematical formula the malware uses to validate its binary payloads. 
4. **Adversarial Payload Detector:** Based on your findings, write a Python CLI tool at `/home/user/app/detector.py` that parses a payload file and detects whether it is a malicious payload from this actor. 
   - Signature: `python3 /home/user/app/detector.py <input_file>`
   - The script must exit with code `1` (and print "EVIL") if the file is malicious, and exit with code `0` (and print "CLEAN") if the file is benign.
   - The payload format requires parsing binary headers where edge cases exist (e.g., malformed length prefixes). The correct formula from the DB must be implemented to verify the checksum.

Ensure that the Nginx service (port 8080) can successfully process a request through to Flask (port 5000) and Redis (port 6379) without hanging.