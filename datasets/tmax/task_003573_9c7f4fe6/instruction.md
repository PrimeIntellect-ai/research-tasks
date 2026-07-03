You are a security engineer tasked with rotating credentials for an internal service. During your audit, you discovered a suspicious legacy bash script used for credential management that might contain a backdoor. You need to investigate the script, identify if it has been exploited, test the vulnerability, and finally rotate the credentials securely.

Perform the following tasks using Bash and standard Linux command-line tools:

1. **Reverse Engineering:** 
   Analyze the obfuscated script located at `/home/user/legacy_rotator.sh`. Identify the hidden backdoor password and the mechanism it uses to execute arbitrary commands.

2. **Log Parsing and Correlation:**
   Analyze the authentication log file at `/home/user/auth.log`. Find the IP address of the attacker who successfully triggered the backdoor. Save this single IP address to `/home/user/compromised_ip.txt`.

3. **Exploit Crafting:**
   To prove the vulnerability exists, craft a bash script at `/home/user/exploit_test.sh` that executes `/home/user/legacy_rotator.sh`. Your script must pass the correct backdoor password and a payload that prints exactly the string `SYSTEM_COMPROMISED` to standard output.

4. **Credential Rotation:**
   Write a bash script at `/home/user/rotate.sh` that performs the actual credential rotation. The script must:
   - Accept exactly one argument: the new password.
   - Update the file `/home/user/config.json`, replacing the value of the `password` field with the newly provided password (do not alter the rest of the JSON structure).
   - Completely delete the vulnerable `/home/user/legacy_rotator.sh` script.

Ensure all created scripts (`exploit_test.sh` and `rotate.sh`) have executable permissions (`chmod +x`). All files must be in `/home/user`.