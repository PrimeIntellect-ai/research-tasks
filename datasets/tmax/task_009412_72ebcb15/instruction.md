You are a forensics analyst investigating a recent security breach on a Linux-based web server. The incident response team has captured the web server's access logs and placed them in `/home/user/web_traffic.log`.

Preliminary analysis suggests that an external attacker successfully exploited a Cross-Site Scripting (XSS) vulnerability to steal sensitive data from an administrator's active session. The attacker injected a malicious payload, which later caused the victim's browser to exfiltrate encrypted data back to the server's logs via a rogue endpoint request.

Your task is to analyze the logs using standard Bash shell commands and built-in utilities to achieve the following:

1. **Identify the Attacker:** Parse the log file to find the IP address that injected the XSS payload. The malicious request contains HTML script tags (either literal `<script>` or URL-encoded like `%3Cscript%3E`). Save *only* this IP address to `/home/user/attacker_ip.txt`.

2. **Extract and Decrypt the Payload:** 
   - The injected script forced the victim's browser to send a GET request to the `/exfil` endpoint with the stolen data in a parameter named `data` (i.e., `/exfil?data=...`).
   - Extract this exfiltrated payload from the log.
   - The payload string is Base64 encoded.
   - Once Base64 decoded, the resulting raw bytes are obfuscated using a single-byte XOR cipher.
   - You must write a bash script or use standard CLI tools to brute-force the XOR key. You know that the decrypted plaintext represents a standard flag format and starts exactly with the string `FLAG{`.

3. **Recover the Evidence:** Once you have successfully determined the correct XOR key and decrypted the message, save the exact decrypted plaintext flag to `/home/user/flag.txt`.

Constraints & Formatting:
- Do not install any external tools. Use standard bash features, coreutils, or common pre-installed Linux binaries (like `base64`, `grep`, `awk`, `sed`, `xxd`, etc.).
- The file `/home/user/attacker_ip.txt` must contain exactly one line with the IPv4 address.
- The file `/home/user/flag.txt` must contain exactly the decrypted flag string (e.g., `FLAG{...}`) with no trailing spaces.