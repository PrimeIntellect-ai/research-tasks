You are a security engineer responsible for rotating credentials for an internal service and auditing its deployment configuration. 

You have been given a compiled ELF binary, `/home/user/rotator`, which handles the credential rotation. This legacy binary enforces a strict policy: it will only accept a new credential if the SHA256 hash of the credential file's exact contents matches one of the pre-approved cryptographic hashes hardcoded within the binary itself.

Additionally, a previous engineer left a deployment script at `/home/user/deploy.sh`. You suspect this script introduces a severe privilege escalation vulnerability into the system if executed by an administrator.

Your task consists of three parts:

1. **Binary Analysis & Cryptographic Hashing**
   - Analyze the ELF binary `/home/user/rotator` to locate the hardcoded, pre-approved SHA256 hashes (they are stored as standard hex strings in the binary).
   - You have been provided a directory `/home/user/candidates/` containing 50 potential credential files (`cred_1.txt` through `cred_50.txt`).
   - Write a Python script to compute the SHA256 hash of each candidate file and determine which candidate's hash matches one of the pre-approved hashes extracted from the binary.
   - Once found, copy the matching candidate file to `/home/user/selected_credential.txt`.

2. **Privilege Escalation Auditing**
   - Audit the script `/home/user/deploy.sh`.
   - Identify the single line of bash code that introduces a local privilege escalation vulnerability (specifically, a configuration that would allow an unprivileged user to escalate to root by exploiting file permissions).
   - Create a file at `/home/user/privesc_vuln.txt` and write *exactly* and *only* the vulnerable line of code into it (preserve original spacing).

Ensure you leave the files `/home/user/selected_credential.txt` and `/home/user/privesc_vuln.txt` precisely as requested, as these will be automatically verified.