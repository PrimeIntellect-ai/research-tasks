You are a forensics analyst responding to a compromised Linux host. The threat actor left behind a compiled executable and a series of exported data logs. Your goal is to reverse-engineer the attacker's tool, identify the compromised service, and safely recover the exfiltrated logs without triggering booby-trapped payloads.

**Phase 1: Binary Analysis and Service Auditing**
The attacker left a stripped ELF binary at `/app/artifact_dumper`. This tool was used to connect to a hidden local service, authenticate, and dump database records.
1. Analyze the stripped binary to determine the exact local TCP port it attempts to connect to.
2. Write the port number (just the integer) to `/home/user/compromised_port.txt`.

**Phase 2: Log Sanitization and Payload Detection**
The attacker's dumped logs contain sensitive user data. Furthermore, the attacker intentionally poisoned some log entries with Cross-Site Scripting (XSS) and SQL Injection (SQLi) payloads designed to compromise forensic analysis tools. 

You must write a Python 3 script at `/home/user/sanitizer.py` to safely process these logs. 
Your script must accept a file path via the `--input` argument, like so:
`python3 /home/user/sanitizer.py --input /path/to/logfile.txt`

The script must enforce the following rules:
1. **Malicious Payload Detection:** The script must analyze the file's contents for common XSS tags (e.g., `<script>`, `javascript:`, `onerror=`) and SQL injection patterns (e.g., `' OR 1=1`, `UNION SELECT`, `--`). If ANY malicious payload is detected, the script MUST immediately exit with status code `1` and print "MALICIOUS" to stdout.
2. **Sensitive Data Redaction:** If the log is benign, the script must scan the text for US Social Security Numbers (format: `XXX-XX-XXXX`) and replace them with the exact string `[REDACTED]`. 
3. **Safe Output:** If the log is benign, the script must print the redacted text to stdout and exit with status code `0`.

Ensure your regex and detection logic is robust. Your script will be tested against a massive suite of both clean logs and highly evasive malicious payloads.