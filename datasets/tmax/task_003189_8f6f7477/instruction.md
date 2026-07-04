As a DevSecOps engineer, you are investigating an incident and enforcing a new Policy-as-Code standard. You have been provided with an incident screen recording (`/app/incident_record.mp4`) and an encrypted policy definition file (`/app/policy_def.enc`). 

Your objectives are to analyze the incident, decrypt the policy, and implement a shell-based request auditing script.

Phase 1: Video Analysis and Decryption
1. The video `/app/incident_record.mp4` shows a developer reproducing an Open Redirect and XSS vulnerability in our login flow. Using `ffmpeg` and any standard CLI tools, analyze the video frames to find a terminal window.
2. The terminal window displays a specific `curl` command exploiting the Open Redirect. Find the exact value assigned to the `redirect_uri` parameter in that `curl` command.
3. The developer's SSH/encryption password is known to follow the format: `DevSecOps_<first_6_characters_of_redirect_uri>`.
4. Decrypt the policy file using standard OpenSSL (AES-256-CBC, PBKDF2). Run: 
   `openssl enc -d -aes-256-cbc -pbkdf2 -in /app/policy_def.enc -out /home/user/policy.txt -pass pass:<derived_password>`

Phase 2: Policy Enforcement Implementation
Read the decrypted `/home/user/policy.txt`. It contains strict specifications for an automated log analyzer. You must implement this analyzer strictly in Bash.
1. Create an executable bash script at `/home/user/enforce_policy.sh`.
2. The script must accept exactly one argument: a raw HTTP request string (e.g., `GET /login?redirect_uri=http://evil.com HTTP/1.1\nCookie: session=xyz`).
3. The script must evaluate the string against the following rules in this exact order of precedence, printing ONLY the rule name to standard output and then exiting:
   - Priority 1 (Open Redirect): If the string contains the exact substring `redirect_uri=http://` or `redirect_uri=https://`, output `CWE-601`.
   - Priority 2 (XSS): If the string contains the exact substring `<script>` or `javascript:`, output `CWE-79`.
   - Priority 3 (Auth Bypass): If the string contains the exact substring `X-Admin-Access: true` AND the substring `Cookie: bypass=`, output `AUTH_BYPASS`.
   - Priority 4 (Default): If none of the above conditions are met, output `SAFE`.
4. Ensure your script handles arbitrary printable ASCII inputs safely without executing malicious code or syntax errors. Only use standard bash built-ins or coreutils.

Your script `/home/user/enforce_policy.sh` will be extensively fuzzed with thousands of generated HTTP requests and its output compared bit-for-bit against our reference implementation to ensure perfect policy compliance.