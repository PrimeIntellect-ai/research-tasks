You are an incident responder investigating a compromised server. We suspect an attacker has modified a custom CGI login binary to include an open redirect vulnerability that steals user tokens, and they may have left an SSH backdoor. 

Please perform the following remediation and investigation steps in the `/home/user/incident` directory:

1. **Binary Analysis:** Examine the compiled ELF binary `/home/user/incident/login.cgi`. The attacker hardcoded a malicious URL starting with `http://` and ending with `/steal?token=` into this binary. Identify the attacker's exact domain from this URL.
2. **SSH Hardening:** Audit the file `/home/user/incident/authorized_keys`. The attacker has appended their own public key. The comment at the end of the attacker's key contains the malicious domain you identified in step 1. Remove this compromised key and save the cleaned file to `/home/user/incident/authorized_keys.safe` (preserve the order of the remaining valid keys).
3. **Secure Coding (C):** Write a new C program at `/home/user/incident/safe_redirect.c` to handle future redirects securely. 
   - The program must take exactly one command-line argument (the target URL).
   - If the URL starts exactly with `https://safe.example.com/`, it should print `Location: <url>` followed by two newline characters (`\n\n`).
   - For any other input (or if no arguments are provided), it must print `Location: https://safe.example.com/error\n\n`.
   - Compile this program to an executable named `/home/user/incident/safe_redirect` using `gcc`.
4. **Content Security Policy:** To prevent further cross-site scripting and unauthorized data exfiltration, create a file `/home/user/incident/csp.txt` that contains exactly one line with the following Content Security Policy header:
   `Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none'; base-uri 'none';`

Ensure all paths are strictly adhered to. You do not need root access for any of these tasks.