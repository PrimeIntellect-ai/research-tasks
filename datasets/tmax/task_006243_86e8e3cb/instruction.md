You are a DevSecOps engineer performing a post-incident audit. We suspect an attacker bypassed our authentication system by exploiting a JWT validation flaw (specifically, the `alg=none` vulnerability) and subsequently altered system configurations to maintain access and escalate privileges. 

You need to perform a three-phase audit and data processing task.

**Phase 1: JWT Log Analysis**
We have a log file of recent authentication tokens at `/home/user/auth_logs.jsonl`. Each line is a JSON object containing a `token` field (the JWT string). 
1. Write a Python script named `/home/user/analyze_jwt.py` to parse these logs.
2. Identify any JWTs where the decoded header specifies `"alg": "none"` (case-insensitive).
3. Extract the `"sub"` (subject) claim from the payload of these vulnerable tokens.
4. Output the unique list of compromised subjects to `/home/user/compromised_subs.txt`, sorted alphabetically, with one subject per line.

**Phase 2: SSH Key Hardening Audit**
The attacker may have dropped or modified SSH keys. 
1. Inspect the directory `/home/user/ssh_keys/`.
2. Find any private key files (files starting with `id_`) that have unsafe permissions (i.e., any permissions broader than `600` / `-rw-------`).
3. Save the absolute paths of these vulnerable key files to `/home/user/weak_ssh_keys.txt`, one per line, sorted alphabetically.

**Phase 3: Privilege Escalation Auditing**
The attacker likely modified automated scripts to establish a privilege escalation path.
1. Inspect the directory `/home/user/scripts/`.
2. Find any regular file in this directory that is world-writable.
3. Calculate the SHA256 checksum of this file.
4. Save the result to `/home/user/privesc_vuln.txt` in the standard `sha256sum` output format (e.g., `[hash]  [absolute_file_path]`).

Ensure all output files are created exactly at the specified paths. You may use standard Linux command-line utilities alongside your Python script to accomplish these tasks.