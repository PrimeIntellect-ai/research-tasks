You are a security engineer responding to a suspected compromise on a Linux server. An attacker exploited a path traversal vulnerability in a file upload handler to steal credentials and leave a staging payload. You need to investigate the incident, decode the attacker's artifacts, and write a Rust utility to rotate the compromised credentials securely.

Your objectives are:

1. **Log Parsing & Correlation**: Analyze the web server log at `/home/user/web_server.log`. Identify the path traversal attack (look for typical `../` patterns) to determine which credential backup file the attacker exfiltrated.
2. **Password Cracking**: The exfiltrated credential file is located at the path discovered in the log (relative to the root of the file system, but it actually resides within `/home/user/`). It contains a SHA-256 hash. Use the dictionary provided at `/home/user/wordlist.txt` to brute-force and find the plaintext password.
3. **Payload Decoding**: The logs also indicate the attacker uploaded a file named `payload.enc` to `/home/user/`. This payload contains the attacker's staging IP address. The attacker obfuscated this file by first XORing the ASCII bytes of the IP address with the hex key `0x5A`, and then Base64 encoding the result. Decode it to retrieve the IP address.
4. **Credential Rotation Tool**: Write a Rust application in `/home/user/rotator` (using `cargo new rotator`). The application must compile and run using `cargo run`. 
   The program must accept exactly three command-line arguments in this order:
   `cargo run -- <cracked_plaintext_password> <decoded_attacker_ip> <new_password>`
   
   The Rust program must:
   - Calculate the SHA-256 hash of the `<new_password>`.
   - Write a log file directly to `/home/user/rotation.log` exactly matching this format:
     ```
     COMPROMISED_PASS: {cracked_plaintext_password}
     ATTACKER_IP: {decoded_attacker_ip}
     NEW_PASS_HASH: {sha256_of_new_password}
     ```

To complete the task:
- Run your Rust program using the cracked password from step 2, the decoded IP from step 3, and the new password `SecureRotation2024!`.
- Ensure `/home/user/rotation.log` is generated correctly.