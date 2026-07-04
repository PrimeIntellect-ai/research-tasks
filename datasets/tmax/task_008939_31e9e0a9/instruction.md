You are an incident responder investigating a recent security breach on an internal Linux server. You have been assigned to analyze an isolated authentication component suspected of containing a vulnerability.

All your work will take place in the directory: `/home/user/incident_014/`

You are provided with two files in this directory:
1. `auth_module.pyc`: A compiled Python bytecode file representing the custom JWT-like verification module used by the application.
2. `auth.log`: A log file containing recent authentication attempts. Each line follows the format:
   `[TIMESTAMP] IP=<IP_ADDRESS> User=<USERNAME> Status=<Success|Failed> Token=<TOKEN_STRING>`

Your objectives are:
1. **Reverse Engineer the Module**: Use Python's built-in `dis` module (or similar techniques) to disassemble and analyze `auth_module.pyc`. Identify the logic flaw that allows an attacker to bypass the signature verification.
2. **Identify Compromised Accounts**: Using the vulnerability you discovered, analyze `auth.log` to determine which IP addresses successfully authenticated as the user `admin` by exploiting this specific bypass vulnerability (i.e., they bypassed the signature check, rather than using a legitimately signed token). 
   - Write the list of these exploited IP addresses to `/home/user/incident_014/compromised_ips.txt`.
   - The file must contain exactly one IP address per line, sorted in ascending order.
3. **Demonstrate the Exploit**: Write a Python script named `/home/user/incident_014/forge.py` that generates a forged token for the user `root` using the bypass technique you identified. 
   - The script must print only the forged token to standard output.
   - Run your script and save the output to `/home/user/incident_014/forged_token.txt`.

Constraints:
- Do not attempt to install external libraries like `PyJWT`; the custom module relies purely on standard library functions (`base64`, `json`, `hmac`, `hashlib`).
- Ensure padding is handled correctly in your forged token (base64url encoding without padding characters `=`).