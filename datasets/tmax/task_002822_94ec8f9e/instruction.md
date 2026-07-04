We have an incident on our hands. A custom, closed-source logging and file hashing utility (`/app/log_hasher`) has been deployed on our server to verify the integrity of uploaded files. However, an attacker recently managed to read sensitive system files, and we suspect this utility is vulnerable to a path traversal or injection attack when processing filenames from the logs. 

Unfortunately, the original developer left, and we only have a stripped binary of the utility.

Your task is to investigate this incident and create a secure replacement for the utility in Python.

Here are the steps you must take:
1. **Analyze the Logs**: Review the security logs in `/var/log/upload_events.log`. Extract the filenames that the attacker attempted to process.
2. **Reverse Engineer the Binary**: The binary `/app/log_hasher` takes a single argument (a filename) and outputs a custom hash. It appears to be vulnerable to path traversal. Analyze the binary to figure out exactly how the custom hashing algorithm works and how the vulnerability is triggered.
3. **Reimplement and Secure**: Write a Python script at `/home/user/secure_hasher.py` that implements the exact same custom hashing algorithm as the binary for valid files, but safely rejects any filenames containing path traversal sequences (like `../`) or command injection characters. The script must accept a filename as a command-line argument and print only the resulting hash to stdout. If the input is invalid/malicious, it must print `ERROR`.

Your Python implementation must be highly efficient. It will be tested against a large dataset of files to ensure it matches the original binary's hashing output (for safe files) and meets a strict performance threshold.

Ensure your script is executable and has the correct shebang.