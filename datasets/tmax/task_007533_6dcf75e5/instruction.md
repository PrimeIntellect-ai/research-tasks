You are acting as a DevSecOps engineer. We have a file upload system that places newly uploaded files into a quarantine directory before they are processed. Recently, we suspect attackers have been uploading files containing path traversal payloads, and users have been accidentally uploading files with unencrypted credit card numbers. 

Your task is to write a Bash script at `/home/user/enforce_policy.sh` that processes these uploads. 

The uploaded files are stored in `/home/user/quarantine/`.
There is a log file at `/home/user/upload_log.csv` which contains the metadata of these uploads. The format is:
`filename,ip_address,timestamp`

Your script must perform the following actions:
1. Read through all files in the `/home/user/quarantine/` directory.
2. **Intrusion Detection**: Scan the contents of each file for path traversal payloads. Consider any file containing the exact strings `../`, `..%2f`, `%2e%2e%2f`, `%2e%2e/`, or `..\` as malicious.
3. **Firewall Policy Generation**: If a file is malicious, you must find the IP address that uploaded it (using `upload_log.csv`). 
   - Append the malicious IP address to `/home/user/malicious_ips.txt` (one IP per line, unique IPs only, sorted ascending).
   - Generate an iptables rules file at `/home/user/block_rules.ipv4` that blocks incoming traffic from these IPs. The file should contain rules in the exact format: `-A INPUT -s <IP_ADDRESS> -j DROP` (one rule per blocked IP, sorted by IP).
   - Delete the malicious file from the quarantine directory.
4. **Data Encryption**: For files that are *not* malicious, scan their contents for 16-digit credit card numbers (the exact regex pattern `\b[0-9]{16}\b`). 
   - If a file contains a credit card number, encrypt it using `openssl enc -aes-256-cbc -pbkdf2 -pass pass:DevSecOps2024! -in <original_file> -out /home/user/secure_vault/<filename>.enc`.
   - Delete the original file from the quarantine directory.
5. **Clean Files**: If a file is neither malicious nor contains credit card numbers, simply move it to `/home/user/clean_uploads/`.

Ensure all necessary output directories (`/home/user/secure_vault/` and `/home/user/clean_uploads/`) are created by your script if they don't exist. Your script should be executable and run without any arguments. Once you have written the script, execute it so the automated tests can verify the final state of the system.