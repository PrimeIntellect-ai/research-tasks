You are a network security engineer investigating a local data exfiltration incident. We suspect an attacker exploited a path traversal vulnerability in a local file handler service to steal sensitive files. 

Your environment contains the following:
1. A vulnerable service currently running on `http://127.0.0.1:8080`.
2. A Base64-encoded packet payload log at `/home/user/traffic_log.b64` which captured the attacker's HTTP request.
3. An exposed private key at `/home/user/target_rsa` that the attacker managed to read.

Perform the following tasks to analyze the attack, demonstrate the vulnerability, and secure the compromised assets:

**Step 1: Payload Decoding & Vulnerability Analysis**
Analyze `/home/user/traffic_log.b64`. The decoded log contains an HTTP GET request with a URL-encoded path traversal payload used by the attacker to steal the `target_rsa` key. 

**Step 2: Automated Vulnerability Scanning**
Write a Python script at `/home/user/scanner.py`. This script must connect to `http://127.0.0.1:8080` and use the same path traversal vulnerability (adjusting the payload) to read the contents of `/home/user/secret_token.txt`. 
The script should output the retrieved file content and also save it exactly as it was received to `/home/user/recovered_token.txt`.

**Step 3: SSH Hardening and File Access Control**
The exposed key at `/home/user/target_rsa` currently has insecure file permissions. Fix its permissions so that only the owner can read or write to it (standard secure permissions for an SSH private key).
Finally, create an SSH client configuration snippet at `/home/user/ssh_config_harden`. The file must contain a configuration block for the host `target-server` that:
- Sets the `IdentityFile` to `/home/user/target_rsa`
- Explicitly disables password authentication by setting `PasswordAuthentication` to `no`

Ensure your `scanner.py` runs successfully and all output files have the correct format and content.