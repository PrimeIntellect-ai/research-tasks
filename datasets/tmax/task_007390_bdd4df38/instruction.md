You are acting as a penetration tester responding to a recent intrusion. You have been provided with server logs, a captured password hash, and a wordlist. Your objective is to correlate the attacker's activity from the logs, extract their session salt, and crack the admin password. 

Write a Go program (which you can save as `/home/user/analyze.go` and run) to perform the following:

1. **Log Parsing and Pattern Matching:** 
   Read `/home/user/server.log`. This file contains JSON-formatted log entries, one per line.
   You must find the IP address of the attacker. The attacker is the uniquely identifiable IP address that successfully accessed the endpoint `/admin/secret_config.json` with an HTTP `status` of `200`. 
   
2. **Salt Extraction:**
   From that exact successful attack log entry, extract the value of the `session_id` field. The attacker used this session ID as a cryptographic salt when they dumped the admin credentials.

3. **Password Cracking:**
   Read the admin's password hash from `/home/user/shadow.txt`. The file contains a single line in the format: `admin:<hex-encoded-sha256-hash>`.
   Using the dictionary file located at `/home/user/wordlist.txt`, perform a dictionary attack to find the plaintext password. 
   The hashing mechanism used is: `SHA256(session_id + password)` (i.e., the string concatenation of the `session_id` and the `password`, with no delimiters, hashed via SHA-256).

4. **Reporting:**
   Create a final report at `/home/user/report.txt` containing exactly two lines in the following format:
   ```
   Attacker IP: <extracted_ip>
   Cracked Password: <cracked_password>
   ```

Requirements:
- You must use Go to parse the logs, perform the pattern matching, and implement the brute-force password cracking logic.
- Do not use external Go packages outside the standard library.
- Ensure the output file `/home/user/report.txt` matches the requested format exactly.