You are a network security engineer investigating a series of suspicious web requests on your company's server. You have been provided with an access log and a cryptographic key, and you must analyze the traffic, decrypt the malicious payload, and generate mitigation configurations.

All your work will take place in the `/home/user/` directory.

**Step 1: Log Parsing and Correlation**
You have a web server access log located at `/home/user/traffic.log`. 
Identify the single IP address that successfully submitted a GET request containing a `token=` parameter in the URL. 
Write this exact IP address to `/home/user/malicious_ip.txt`.

**Step 2: Decryption and Exploit Analysis**
The value of the `token=` parameter you found is a base64-encoded, AES-256-CBC encrypted exploit payload. 
The encryption uses PBKDF2. The password to decrypt this payload is stored in plain text in the file `/home/user/secret.key`.
Decrypt the token. The decrypted plaintext is an HTML snippet containing an XSS exploit (a `<script>` tag). 
Extract the malicious domain name (e.g., `attacker.com` from `src="https://attacker.com/script.js"`) from the decrypted payload.
Write ONLY the extracted malicious domain to `/home/user/malicious_domain.txt`.

**Step 3: Content Security Policy (CSP) Enforcement**
To prevent this type of XSS execution in the future, define a strict Content Security Policy.
Create a file at `/home/user/csp_header.txt` containing exactly the following CSP directive (on a single line):
A policy that restricts all default behavior to none (`default-src 'none';`), restricts scripts to only the same origin (`script-src 'self';`), and restricts styles to the same origin (`style-src 'self';`).

**Step 4: Network Policy Configuration**
To block the offending IP address at the reverse proxy level, write a Bash script at `/home/user/generate_block_rule.sh`.
The script must take a single IP address as its first positional argument (`$1`) and print an Nginx deny rule to standard output in the exact format:
`deny <IP_ADDRESS>;`
Ensure the script is executable.

Ensure all output files (`malicious_ip.txt`, `malicious_domain.txt`, `csp_header.txt`, `generate_block_rule.sh`) are placed directly in `/home/user/` with the exact requested names.