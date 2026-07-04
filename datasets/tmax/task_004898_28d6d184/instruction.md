You are an incident responder investigating a suspected breach on a web server. The server owner provided an archive of their web directory, the SSL certificate found on the server, a list of known-good file hashes, and recent access logs. They suspect an attacker modified a web asset, swapped the SSL certificate to intercept internal API calls, and left traces in the logs.

Your task is to write a Bash script at `/home/user/analyze.sh` that automates the investigation of these files and outputs a final report to `/home/user/report.txt`.

You have the following files available:
1. `/home/user/server_data/hashes.txt`: Contains the SHA256 hashes of the original, unmodified web files in standard `sha256sum` output format.
2. `/home/user/server_data/www/`: The directory containing the current web files. Exactly one file here has been modified by the attacker.
3. `/home/user/server_data/cert.pem`: The X.509 certificate currently installed on the server.
4. `/home/user/server_data/access.log`: The web server access log in standard combined format.

Your script `/home/user/analyze.sh` must perform the following actions:
1. **File Integrity Verification**: Compare the files in `/home/user/server_data/www/` against `/home/user/server_data/hashes.txt` to identify the single modified file.
2. **TLS Certificate Analysis**: Extract the Common Name (CN) of the **Issuer** from `/home/user/server_data/cert.pem`.
3. **Intrusion Detection**: Analyze `/home/user/server_data/access.log`. Find the IP address that accessed the compromised file (identified in step 1) AND whose request contains the suspicious pattern `base64_decode(` in the URL.

The script must write the findings to `/home/user/report.txt` in the following exact format:
```
COMPROMISED_FILE: <filename_only>
ROGUE_ISSUER: <issuer_common_name>
ATTACKER_IP: <ip_address>
```

Requirements:
- Your script must be executable and runnable without arguments.
- Extract *only* the filename for the COMPROMISED_FILE field (e.g., `script.js`, not the full path).
- The rogue issuer CN should be the exact string value of the CN field.
- The attacker IP must be extracted precisely from the log line matching the conditions.