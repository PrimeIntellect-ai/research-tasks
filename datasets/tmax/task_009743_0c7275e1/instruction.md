You are a security engineer tasked with rotating credentials following a recent phishing incident. Attackers exploited an open redirect vulnerability in a legacy authentication service to steal user passwords.

Your goal is to identify the compromised accounts, reverse engineer the legacy authentication binary to discover its password hashing scheme, and crack the stolen passwords using a provided wordlist. Finally, you will output a report of the compromised credentials.

Here are the details of your environment and task:

1. **Log Analysis:** 
   Analyze the web server access logs located at `/home/user/auth.log`. The logs follow a custom format:
   `[TIMESTAMP] IP METHOD URL STATUS "payload"`
   Attackers used the open redirect vulnerability by passing an external URL to the `next` parameter (e.g., `/login?next=http://malicious.example.com`). Identify all usernames that successfully authenticated (STATUS `200`) in requests that contained a malicious open redirect (an external HTTP/HTTPS URL in the `next` parameter, rather than a relative path).

2. **Reverse Engineering:**
   The legacy authentication service binary is located at `/home/user/auth_server`. It is a compiled Rust ELF executable. 
   The service hashes passwords using SHA-256, but it appends a hardcoded "pepper" (a secret string) to the password before hashing. 
   Analyze the binary (e.g., using `strings`, `objdump`, or similar tools) to extract this hardcoded pepper. It is a 16-character string.

3. **Password Cracking:**
   A database dump of all current usernames and their corresponding password hashes is located at `/home/user/users.txt`, formatted as `username:hash`.
   A wordlist of common passwords is provided at `/home/user/wordlist.txt`.
   
   Write a Rust program in `/home/user/cracker` (initialize a new cargo project here) that:
   - Reads the compromised usernames identified in step 1.
   - Reads the corresponding hashes from `/home/user/users.txt`.
   - Uses the hardcoded pepper discovered in step 2 to crack the passwords of *only* the compromised users, using the words in `/home/user/wordlist.txt`. 
   
4. **Reporting:**
   Output the cracked credentials for the compromised users to a JSON file located at `/home/user/cracked.json`.
   The format must be a single JSON object mapping usernames to their plaintext passwords:
   ```json
   {
     "username1": "plaintext_password",
     "username2": "plaintext_password"
   }
   ```

Complete all phases. To verify your work, an automated test will check the exact contents of `/home/user/cracked.json`.