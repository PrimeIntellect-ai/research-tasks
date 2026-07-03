You are a DevSecOps engineer tasked with enforcing a strict file integrity policy as code, while auditing and replacing a vulnerable legacy script.

A previous engineer recorded a terminal session demonstrating the deployment of our new policy framework, but they left the company before documenting the password. The recording is available at `/app/audit_recording.mp4`. 

Your tasks are as follows:

1. **Extract the Admin Hash:** Analyze `/app/audit_recording.mp4`. The video contains an embedded subtitle/metadata track that displays the administrator login hash. Extract this text.
2. **Crack the Password:** The extracted string is an MD5 hash of the admin password. Use the provided DevSecOps dictionary located at `/app/wordlist.txt` to crack the hash.
3. **Decrypt the Policy:** Use the cracked password to decrypt the file integrity policy using OpenSSL (AES-256-CBC, pbkdf2). The encrypted policy is at `/app/policy.enc`. Save the decrypted file exactly to `/home/user/policy.txt`. This file contains a list of approved SHA256 checksums (one per line).
4. **Audit and Replace the Legacy Script:** We previously used a shell script to check directory integrity, but it was flagged in an audit for CWE-78 (OS Command Injection) because it failed to safely handle filenames containing shell metacharacters (e.g., spaces, quotes, semicolons, newlines). 
5. **Implement `secure_checker.sh`:** Write a new, secure Bash script at `/home/user/secure_checker.sh` that takes a single directory path as an argument. 
   - The script must iterate over all standard files in the provided directory.
   - For each file, compute its SHA256 hash.
   - If the hash exists in `/home/user/policy.txt`, the script must print: `[OK] <filename>`
   - If the hash does NOT exist in the policy, print: `[FAIL] <filename>`
   - The output lines must be printed in alphabetical order based on the `<filename>`.
   - **Security Requirement:** Your script must be strictly immune to command injection. It will be tested against maliciously crafted filenames.

Make sure your script at `/home/user/secure_checker.sh` is executable. We will use an automated fuzzer to verify that your script's behavior is bit-exact equivalent to our hidden reference implementation (`/app/oracle_checker`) across dozens of edge-case inputs.