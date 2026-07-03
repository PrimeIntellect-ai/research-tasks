You are an incident responder investigating a compromised web server. The server has been taken offline, and you have been provided with a snapshot of the application source code and some encrypted evidence left behind by the attacker.

Your investigation consists of four phases:

**Phase 1: Source Code Auditing and CWE Identification**
The web application source code is located at `/home/user/app/server.py`. Review the code to identify the two major security vulnerabilities present in the web endpoints. You need to classify these vulnerabilities using their official CWE (Common Weakness Enumeration) IDs (e.g., "CWE-22" for Path Traversal). The application is known to suffer from an injection vulnerability and a cross-site scripting vulnerability.

**Phase 2: Cryptographic Key Extraction and Decryption**
The attacker encrypted their staging logs to hide their activities. The encrypted log file is located at `/home/user/evidence/staging_logs.enc`. 
During your code review in Phase 1, you will notice that the application uses symmetric encryption (Fernet) for cookie management, and the secret key is hardcoded in `server.py`. 
Use this key to write a Python script that decrypts `/home/user/evidence/staging_logs.enc`. Extract the plaintext log contents.

**Phase 3: Service Auditing and Port Scanning**
The decrypted log indicates that the attacker successfully spawned a hidden backdoor service locally on the server. The log doesn't specify the exact port, but intelligence suggests the backdoor listens on a TCP port between `13000` and `13050`. 
Write a Python script to scan the `localhost` TCP ports in the range `13000-13050` to identify the exact port where the backdoor is currently running. 

**Phase 4: Incident Reporting**
Compile your findings into a structured JSON report located at `/home/user/incident_report.json`. The JSON file must strictly follow this structure:
```json
{
  "cwe_vulnerabilities": ["CWE-XX", "CWE-YY"],
  "decrypted_log_secret": "<the exact string value of the 'SECRET_FLAG' field found inside the decrypted log>",
  "backdoor_port": <integer of the open backdoor port>
}
```
*Note: Sort the CWE IDs in the list in ascending alphabetical order.*