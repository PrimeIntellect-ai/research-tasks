You are a penetration tester auditing a custom CGI authentication gateway written in Bash. The developers have asked you to review the source code, identify vulnerabilities, demonstrate an exploit, and document your findings.

You have been provided with the following files:
1. `/home/user/vulnerable_auth.sh` - The authentication script that simulates processing a login request.
2. `/home/user/wordlist.txt` - A dictionary of candidate passwords to use for your audit.

Your objectives:
1. **Code Auditing & CWE Identification**: Analyze `/home/user/vulnerable_auth.sh`. It contains an insecure redirect mechanism (often called an Open Redirect). Identify the standard CWE identifier for this type of vulnerability (format: `CWE-XXX`).
2. **Password Cracking**: The script contains a hardcoded MD5 hash for the `admin` user. Use `/home/user/wordlist.txt` to crack this hash and find the plaintext password.
3. **Payload Encoding**: Construct a URL-encoded payload for the `redirect` parameter that will cause the script to redirect a successful login to exactly `http://malicious.example.com/login`.
4. **Reporting**: Create a JSON file at `/home/user/audit_report.json` containing your findings. It must have exactly the following structure and keys:
   ```json
   {
     "cwe_id": "CWE-XXX",
     "cracked_password": "the_plaintext_password",
     "exploit_payload": "the_url_encoded_payload"
   }
   ```
5. **Exploit Verification Script**: Write a Bash script at `/home/user/verify.sh` that practically demonstrates the exploit against the script. 
   - Your script should set the environment variables `USER_ID`, `PASS_KEY`, and `REDIR_URL` to "admin", your cracked plaintext password, and your URL-encoded exploit payload, respectively.
   - It should then execute `/home/user/vulnerable_auth.sh` and redirect all of its standard output to `/home/user/exploit_result.txt`.
   - Ensure `/home/user/verify.sh` has executable permissions.
   - Run your `verify.sh` script to generate `/home/user/exploit_result.txt`.

Ensure all requested files are created at their exact paths with the correct content.