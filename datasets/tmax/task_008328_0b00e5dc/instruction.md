You are a forensics analyst responding to a security incident on a Linux host. We have isolated a suspicious C++ service that is currently running on the machine, and we suspect the attacker exploited it to store or manipulate evidence in memory. 

Your objective is to audit the provided source code, identify the vulnerability, analyze the intrusion logs, and craft a C++ exploit to recover the evidence from the running service.

Here are the details of the environment and your tasks:

1. **Vulnerability Identification (Code Auditing):**
   The source code for the running service is located at `/home/user/server.cpp`. Review this C++ code to find the vulnerability that allows out-of-bounds memory access.
   - Identify the exact CWE (Common Weakness Enumeration) identifier for this vulnerability.
   - Write the identifier to `/home/user/cwe.txt` in the format `CWE-XXX` (e.g., CWE-999).

2. **Pattern Matching and Intrusion Detection:**
   The attacker previously interacted with this service. We have captured the service's incoming request logs in `/home/user/ids.log`. The log format is `[Timestamp] [IP Address] [Hex Payload]`.
   - The attacker exploited the exact same out-of-bounds read vulnerability.
   - Analyze the log to find the payload that attempts to read beyond the intended bounds of the internal array based on your analysis of `/home/user/server.cpp`.
   - Extract the IP address of the attacker who sent this malicious payload.
   - Save the extracted IP address to `/home/user/attacker_ip.txt`.

3. **Exploit Crafting and Evidence Recovery:**
   The vulnerable service is currently executing and listening on TCP port `9999` on `127.0.0.1`. A critical piece of evidence (a flag) is loaded into the process's memory adjacent to the vulnerable array.
   - Write a C++ program at `/home/user/exploit.cpp`.
   - Your program must connect to `127.0.0.1:9999` and send a crafted binary payload to exploit the out-of-bounds read vulnerability.
   - The program should receive the leaked memory containing the flag and print it to standard output.
   - Compile your exploit and run it. Extract the retrieved evidence flag and save it exactly as it appears to `/home/user/evidence.txt`.

Ensure all requested output files (`cwe.txt`, `attacker_ip.txt`, `evidence.txt`) are created in `/home/user/` and contain only the requested data, with no extra formatting or whitespace.