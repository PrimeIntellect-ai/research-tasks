You are a security engineer tasked with rotating compromised service credentials. Our security monitoring system has flagged several service tokens as leaked.

You must perform the credential rotation using Python. 

Here is the information you have:
1. **Security Log**: `/home/user/security.log` contains recent security events. Look for lines with the exact string `[LEAK_DETECTED]` to identify which services have compromised tokens.
2. **Configuration Integrity**: Before rotating any token, you must ensure the service's configuration file hasn't been tampered with. A list of known-good SHA256 hashes is located at `/home/user/config_hashes.txt`. The configuration files are stored in `/home/user/configs/`. 
3. **Master Key**: The secret key used to sign new tokens is stored in plain text in `/home/user/master.key`.
4. **Token Generation**: For each compromised service with an *intact* configuration file, you must generate a new JSON Web Token (JWT). 
   - The payload must be: `{"service": "<service_name>", "version": 2}`
   - The algorithm must be `HS256`.
   - Use the key found in `/home/user/master.key`.
5. **Configuration Update**: Update the compromised service's JSON configuration file. Replace the value of the `"token"` key with the newly generated JWT. Do not modify any other keys in the JSON file.
6. **Reporting**: Create a report file at `/home/user/rotation_report.txt`. For every service identified as leaked in the log, append a line:
   - If the config file's SHA256 hash matches the one in `config_hashes.txt`, write: `SUCCESS: <service_name>`
   - If the config file's SHA256 hash DOES NOT match, write: `TAMPERED: <service_name>` (and do NOT rotate its token).

Ensure you install any necessary Python packages (like `PyJWT`) in your local environment.