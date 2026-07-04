You are an incident responder investigating a suspected breach of a simple bash-based web service. The web server team noticed anomalous behavior and suspects that an attacker managed to read their TLS private key.

Your workspace is located at `/home/user/web_incident/`. 
Inside this directory, you will find:
- `access.log`: The web server access logs.
- `server.sh`: The backend bash script that processes user input.
- `certs/server.key`: The TLS private key for the server.

Your task consists of four parts:
1. **Log Analysis**: Identify the IP address of the attacker who successfully extracted the private key. The attacker exploited a vulnerability in the `server.sh` script to read `certs/server.key`. Write ONLY the attacker's IPv4 address to `/home/user/web_incident/attacker_ip.txt`.
2. **CWE Identification**: Analyze `server.sh` to determine the underlying vulnerability type. Write the standard CWE identifier (in the format `CWE-XXX`) for this specific vulnerability to `/home/user/web_incident/cwe.txt`. 
3. **Code Remediation**: The `server.sh` script currently accepts a single argument and echoes a welcome message. However, it does so insecurely. Modify `/home/user/web_incident/server.sh` to fix the vulnerability while preserving its exact intended functionality (it should safely output `Welcome [argument]`).
4. **Access Control**: The private key `/home/user/web_incident/certs/server.key` was successfully read because of poor file permissions, on top of the web vulnerability. Secure the private key by setting its file permissions so that it can strictly only be read and written by the owner, with no access for group or others.

Make sure your final outputs exactly match the requested filenames and formats.