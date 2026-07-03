You are a security researcher analyzing a suspicious Python script found on a compromised Linux server. The script seems to masquerade as a routine system metric worker, but occasionally exhibits anomalous behavior. 

Your investigation has two parts:

Part 1: Statistical Anomaly Investigation
You have been provided with a log of the worker's recent executions at `/home/user/sys_metrics.csv`. The CSV has the columns: `timestamp,cpu_usage,mem_usage,execution_duration`. 
Normally, the execution duration is very short (around 0.1 to 0.3 seconds). However, when the malicious payload triggers, the execution duration spikes significantly.
Write a script to analyze this CSV and find the exact `timestamp` of every execution where the `execution_duration` was greater than 4.0 seconds. 
Write these anomalous timestamps to a file located at `/home/user/anomalies.txt`, with one timestamp per line, sorted in chronological order.

Part 2: Intermediate State Tracing & Debugging
The suspicious script is located at `/home/user/suspicious_worker.py`. 
It appears to check for certain environment misconfigurations or specific environment variables before it decrypts its payload and reveals the Command and Control (C2) exfiltration IP address.
Use a Python debugger (`pdb`) or modify the script to trace its intermediate state and figure out what environment variables it requires to trigger the payload, or simply bypass the checks to force the payload decryption in your debugger.
Once you successfully determine the plain-text IPv4 address the script attempts to contact for exfiltration, write ONLY the IP address to `/home/user/exfiltration_ip.txt`.

Ensure both `/home/user/anomalies.txt` and `/home/user/exfiltration_ip.txt` exist and contain the correct values.