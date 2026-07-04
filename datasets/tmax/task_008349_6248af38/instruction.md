You are a security auditor performing a post-mortem analysis on a compromised Linux system. We have extracted snapshots of process data into the directory `/home/user/proc_dumps/`. It is suspected that a misconfigured root-level service leaked an encoded SSH private key through its command-line arguments, which are visible to any user via `/proc`. 

Your goal is to build an automated vulnerability scanner in Python to audit these process dumps, identify the privilege escalation vector, decode the payload, and properly secure the discovered credentials.

Perform the following tasks:

1. **Process Analysis Script**: Write a Python script at `/home/user/audit_procs.py`. This script must:
    * Iterate through all process ID (PID) files in `/home/user/proc_dumps/`. For a given process, you will find two files: `<pid>_cmdline` (simulating `/proc/<pid>/cmdline`) and `<pid>_status` (simulating `/proc/<pid>/status`).
    * Check if the process is running as root (UID 0). The `Uid` line in the status file contains the real, effective, saved set, and filesystem UIDs (e.g., `Uid:	0	0	0	0`).
    * If the process is running as root, parse its `cmdline` file. Command-line arguments in `/proc` are separated by null bytes (`\x00`). 
    * Look for the argument `--auth-token`. The immediately following argument is a Base64-encoded payload.
    * Decode the Base64 payload.

2. **Generate Audit Report**: Your Python script must output its findings to `/home/user/audit_report.json`. The JSON file should contain a list of dictionaries with exactly these keys:
    * `"pid"`: The process ID (integer).
    * `"uid"`: The real UID of the process (integer, should be 0).
    * `"leaked_key"`: The decoded payload string (the SSH key).

3. **SSH Key Management and Hardening**: 
    * Extract the decoded SSH private key found in the root process and save it directly to `/home/user/.ssh/leaked_id_rsa`. 
    * Ensure this file has the strict, correct permissions required by SSH (read/write by owner only).
    * Create an SSH configuration file at `/home/user/.ssh/config`. Configure a host entry named `audit-target` that explicitly uses this key (`IdentityFile`), forces the use of only configured identities (`IdentitiesOnly yes`), and disables password authentication (`PasswordAuthentication no`) to harden the connection against brute force.

Ensure all paths used are absolute. You can use standard bash commands to create directories like `/home/user/.ssh` if they do not exist.