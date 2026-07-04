You are acting as a penetration tester performing a post-incident scan and vulnerability assessment on a compromised local environment. 

You have been provided with some artifacts in your home directory: `/home/user/`.

Your task is to perform the following three actions using Bash and standard Linux tools:

1. **Log Parsing for Intrusion Detection:**
   Analyze the web server log file located at `/home/user/access.log`. Identify the IP address of the attacker who attempted a Log4j (JNDI) injection attack (look for the `jndi:ldap` pattern). Extract ONLY the attacker's IPv4 address and write it to `/home/user/attacker.txt`.

2. **TLS Certificate Inspection:**
   There is a suspicious certificate file left by the attacker at `/home/user/service.pem`. Extract its exact "Not After" expiration date (e.g., `Oct 10 23:59:59 2024 GMT`). Write ONLY this expiration date string to `/home/user/cert_expiry.txt`.

3. **Exploit Crafting (Command Injection):**
   The attacker exploited a local script that executes user input but filters out all space characters ( ). To demonstrate the vulnerability for the report, craft a Bash command injection payload that outputs the contents of `/home/user/secret.key` **without using any space characters** in the payload. (Hint: you can use bash features like redirection or special variables). 
   Write your crafted payload string into `/home/user/payload.txt`. Ensure the file contains nothing but the payload.

Requirements:
- Ensure all output files are placed in `/home/user/`.
- `/home/user/payload.txt` must not contain any spaces.