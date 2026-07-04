You are acting as an incident responder investigating a recent breach on our web server. We suspect the attacker exploited an open redirect vulnerability in our login flow to steal credentials, and then left behind some encrypted artifacts. 

You need to perform the following investigation and remediation steps using Bash commands and scripts:

1. **Payload Decoding**: 
   Review the web server log located at `/home/user/access.log`. The attacker exploited a parameter named `redirect=` in the URL. The value of this parameter is Base64 encoded. 
   Find all requests containing `redirect=`, extract the Base64 encoded payload, decode it, and write the decoded URLs to `/home/user/redirects_decoded.txt`. Each URL should be on a new line. Sort the unique URLs alphabetically.

2. **Password Brute-forcing**:
   The attacker left behind an encrypted archive containing exfiltrated data at `/home/user/exfiltrated.zip`. Use the provided wordlist at `/home/user/wordlist.txt` to brute-force the password of this zip file. Extract the contents of the zip file into a new directory: `/home/user/recovered/`.

3. **Decryption**:
   Inside the `/home/user/recovered/` directory, you will find two files: `key.txt` and `payload.enc`. The file `payload.enc` was encrypted using OpenSSL with the `aes-256-cbc` cipher with PBKDF2. The decryption passphrase is the exact string contained inside `key.txt`. 
   Decrypt `payload.enc` and save the decrypted output to `/home/user/payload_decrypted.txt`.

4. **Access Control Remediation**:
   The attacker messed up the file permissions in the web root directory `/home/user/webroot/`, leaving some files world-writable.
   Create a bash script at `/home/user/fix_perms.sh` that takes a directory path as an argument and recursively sets all directories inside it (including the root directory passed) to permission `755`, and all files to permission `644`. 
   Execute your script on `/home/user/webroot/`: `bash /home/user/fix_perms.sh /home/user/webroot/`

Ensure all output files (`/home/user/redirects_decoded.txt`, `/home/user/payload_decrypted.txt`) are exactly as requested so automated verification can succeed.