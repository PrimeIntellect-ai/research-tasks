You are an incident responder investigating a suspected breach on a Linux server. The initial vector appears to be a local file upload utility `/home/user/upload.py` that handles file staging. We suspect it is susceptible to a path traversal vulnerability. 

The attacker used this vulnerability to overwrite SSH keys and drop a malicious payload. You must perform the following actions:

1. **Verify the Vulnerability:** 
   Demonstrate the path traversal vulnerability in `/home/user/upload.py`. The script accepts two positional arguments: `filename` and `content`. It normally saves files to `/home/user/uploads/`. Use this script to write the exact string `VULN_VERIFIED` into a file located at `/home/user/proof.txt`.

2. **Analyze the Payload:**
   We found a suspicious file at `/home/user/suspicious_bin`. Write a Python script at `/home/user/hash_check.py` that calculates the SHA-256 hash of `/home/user/suspicious_bin` and saves the resulting hex digest as a single line in `/home/user/hash_log.txt`. Run your script to generate the log.

3. **Secure the SSH Configuration:**
   The attacker messed up the permissions on the SSH directory to maintain access. Fix the file permissions for `/home/user/.ssh` and `/home/user/.ssh/authorized_keys` so they comply with standard strict SSH access requirements (directories must only be accessible by the owner, and files only readable/writable by the owner).

Do not change the contents of `upload.py` or `suspicious_bin`. Ensure your output files precisely match the requested names and paths.