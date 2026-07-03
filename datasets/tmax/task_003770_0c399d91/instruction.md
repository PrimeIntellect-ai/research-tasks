You are an incident responder investigating a recent breach on a web server. The attacker managed to execute commands, tamper with a web asset to exfiltrate data, and log out. We have captured a screen recording of the console during the breach.

Your task consists of three phases:

**Phase 1: Video Forensics and Firewall Policy**
1. Analyze the provided video capture of the breach console located at `/app/breach_console.mp4`. The video shows a terminal session where the attacker's connection IP is briefly visible in a log output.
2. Identify the attacker's IPv4 address from the video and save it exactly as a plain string in `/home/user/attacker_ip.txt`.
3. Create a bash script at `/home/user/block_ip.sh` containing the exact `iptables` command required to drop all inbound TCP traffic from the attacker's IP address. (Do not execute the script, as you lack root privileges, just create it).

**Phase 2: File Integrity Verification**
The attacker tampered with one of the files in the web directory `/app/webroot/`. We have a known-good SHA-256 manifest located at `/app/manifest.sha256` (standard `sha256sum` format).
1. Write a C program at `/home/user/check_integrity.c` that programmatically computes the SHA-256 hashes of all files listed in the manifest and compares them against the expected hashes. 
2. Identify the single tampered file. Save its full absolute path to `/home/user/tampered_file.txt`.

**Phase 3: Sensitive Data Redaction**
The tampered file you identified contains a mixed data dump of benign web logs and sensitive customer Credit Card (CC) numbers. 
1. Write a high-performance C program at `/home/user/redact.c` that reads an input file and writes to an output file.
2. The program must detect and redact all 16-digit credit card numbers. Credit card numbers may appear as 16 consecutive digits (e.g., `1234567890123456`), or broken up by spaces or dashes (e.g., `1234-5678-9012-3456` or `1234 5678 9012 3456`).
3. For every matched credit card, replace ONLY the numeric digits with the character `X`, leaving spaces or dashes intact (e.g., `XXXX-XXXX-XXXX-XXXX`). All other numbers and text in the file must remain completely untouched.
4. Compile your program and use it to process the tampered file. Save the sanitized output to `/home/user/redacted_dump.txt`. 

Your redaction program's output will be graded against a perfect golden reference file using a character-level accuracy metric. You must achieve at least 99% accuracy.