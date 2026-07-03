You are acting as a penetration tester and incident responder analyzing a suspected breach.

We have an authentication web server whose source code and recent access logs have been provided to you in `/home/user/workspace`. 

Your objective is to audit the application, identify the vulnerability, find the attacker, and build a detection script.

Perform the following tasks:
1. **Identify the Vulnerability**: Review `/home/user/workspace/app.py`. There is a vulnerability in the authentication flow's redirect mechanism. Identify the specific CWE (Common Weakness Enumeration) identifier for this exact vulnerability. Write ONLY the CWE ID (in the format `CWE-XXX`) to a new file at `/home/user/workspace/cwe.txt`.

2. **Identify the Attacker**: Review `/home/user/workspace/access.log`. Find the IP address of the attacker who successfully exploited this vulnerability to redirect a user specifically to `http://evil.com/phish`. Write ONLY their IP address to `/home/user/workspace/attacker.txt`.

3. **Create a Detection Scanner**: Write a Python script at `/home/user/workspace/detect.py`. The script must:
   - Take exactly one command-line argument: the path to an access log file.
   - Parse the log file to identify any IP addresses that attempted to exploit this vulnerability. 
   - An exploit attempt is defined as any `GET` request to the `/login` endpoint where the `next` query parameter contains an absolute URL starting with `http://` or `https://` (e.g., `?next=http://...` or `?next=https://...`). 
   - Print the unique IP addresses of the attackers to standard output, one per line, sorted in ascending order.

Ensure your Python script handles standard file reading and prints precisely the IP addresses without any additional text.