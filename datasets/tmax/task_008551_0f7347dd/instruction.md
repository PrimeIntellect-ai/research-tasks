You are acting as a forensics analyst tasked with processing evidence from a compromised host. You have been provided with an evidence directory at `/home/user/evidence` and a mock filesystem dump at `/home/user/fs_dump`. The agent compromised the machine and left traces of credential leakage and privilege escalation.

Your task consists of three phases:

**Phase 1: Privilege Escalation Auditing**
The attacker left SUID binaries in the system. Find all files within the directory `/home/user/fs_dump/bin` that have the SUID bit set. Calculate the SHA-256 hash of each SUID file found.
Write the results to `/home/user/suid_hashes.txt` in the following format (one per line, sorted alphabetically by file path):
`<SHA-256 Hash>  <full file path>`

**Phase 2: Sensitive Data Redaction & Hashing (C Programming)**
The attacker captured a process environment dump containing sensitive credentials, located at `/home/user/evidence/environ.txt`. 
You must write a C program at `/home/user/evidence/extractor.c` that does the following:
1. Reads `/home/user/evidence/environ.txt` line by line.
2. Identifies any line starting exactly with `PASSWORD=` and replaces the entire line with `PASSWORD=REDACTED\n`. All other lines should remain unchanged.
3. Writes the processed (redacted) lines to `/home/user/evidence/redacted_environ.txt`.
4. Computes the SHA-256 hash of the exact contents written to `redacted_environ.txt` using the OpenSSL crypto library (`libcrypto`).
5. Writes the resulting SHA-256 hash as a lowercase hex string to `/home/user/evidence/hash.txt`.

You must compile this program to `/home/user/evidence/extractor` and run it. Ensure the OpenSSL development headers are installed and linked properly.

**Phase 3: Network Policy Generation**
Analyze the log file at `/home/user/evidence/syslog`. Find the IP address that successfully connected to the backdoor port `1337`. 
Write a bash script at `/home/user/iptables_rule.sh` containing the exact `iptables` command to drop all incoming TCP traffic from that specific IP address on port `1337` to the local machine. The script must contain exactly one `iptables` command (e.g., `iptables -A INPUT ... -j DROP`). Ensure the script is executable.

Complete all phases and ensure the output files precisely match the specified formats.