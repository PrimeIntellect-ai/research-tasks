You are a forensics analyst investigating a compromised Linux host. The attacker left behind an evidence folder at `/home/user/evidence/`. Your goal is to recover key details about the breach by performing file integrity verification, HTTP log inspection, and writing a password cracker in Go.

You need to complete three forensic objectives and write your findings to a precise report file.

**Objective 1: File Integrity Verification**
The directory `/home/user/evidence/bin/` contains several system binaries. The attacker modified exactly one of these binaries to maintain persistence. You have been provided with a known-good MD5 checksum file at `/home/user/evidence/checksums.md5`. 
Identify the name of the tampered binary (the file whose hash does not match the manifest).

**Objective 2: HTTP Cookie Inspection**
The attacker exfiltrated a privileged session token. You have a snippet of the web server access logs at `/home/user/evidence/access.log`. 
Find the HTTP request made to the endpoint `/exfiltrate` and extract the value of the `session_id` cookie from the HTTP headers recorded in that log entry.

**Objective 3: Password Cracking (Go)**
The attacker left behind a compiled binary that was used to encrypt stolen data, along with its source code snippet in `/home/user/evidence/lock.go` and a hash file `/home/user/evidence/secret.hash`. 
The source code reveals that the attacker used a 4-digit numeric PIN (0000-9999) appended to the salt `SALT_FORENSICS`, and then took the MD5 hash of the resulting string. 
The file `secret.hash` contains the resulting MD5 hash as a hex string.
Write a Go program to brute-force this 4-digit PIN.

**Final Output:**
Create a file at `/home/user/forensics_report.txt` with exactly the following three lines in this order:
Line 1: The name of the tampered binary (just the filename).
Line 2: The exfiltrated session_id cookie value (just the value, e.g., if the cookie is `session_id=12345`, write `12345`).
Line 3: The 4-digit PIN you cracked.