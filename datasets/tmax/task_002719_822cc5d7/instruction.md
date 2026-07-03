You are acting as a penetration tester reviewing a simulated process snapshot from a compromised Linux server. An automated monitoring script captured the output of a `ps` command and saved it to `/home/user/process_dump.txt`. 

Your objectives are to identify leaked credentials and malicious payloads, crack the compromised passwords, and redact the sensitive information to prepare the log for secure reporting.

Perform the following tasks:

1. **Password Cracking:** 
   Analyze `/home/user/process_dump.txt`. You will notice a process running an authentication script that leaks an MD5 hash via command-line arguments.
   Crack this MD5 hash using the provided wordlist located at `/home/user/wordlist.txt`.
   Save the cracked plaintext password to `/home/user/cracked.txt` (the file should contain only the plaintext password and no other text or trailing newlines).

2. **Payload Decoding & Auditing:**
   The process dump also contains a suspicious reverse-shell or privilege escalation payload executed by the `www-data` user, which is base64 encoded.
   Extract and decode this base64 payload. 
   Save the decoded plaintext command to `/home/user/payload.txt` (the file should contain exactly the decoded command).

3. **Sensitive Data Redaction:**
   Prepare a sanitized version of the process dump for the audit report. 
   Create a new file at `/home/user/redacted_dump.txt`. 
   This file must be an exact copy of `/home/user/process_dump.txt`, EXCEPT:
   - The 32-character MD5 hash must be replaced with the exact string `[REDACTED]`.
   - The base64 encoded string used in the `www-data` command must be replaced with the exact string `[REDACTED]`.

Ensure all output files are placed exactly at the paths specified. You may use Bash, Python, or any installed tools to accomplish these tasks.