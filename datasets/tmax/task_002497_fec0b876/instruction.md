You are an incident responder investigating a suspected credential leak on a compromised Linux server. We believe an unauthorized background script is monitoring process execution (via `/proc`) to steal database credentials passed as command-line arguments, and is subsequently exfiltrating them over HTTPS.

Your investigation environment is set up in `/home/user/investigation/`. 
Inside this directory, you will find:
- `processor.py`: Our data processing script that spawns a subprocess (`worker.py`), passing the database user and password as command-line arguments.
- `worker.py`: A dummy worker script that simulates data processing.
- `monitor.py`: The suspected malicious script. It continuously monitors `/proc` for running instances of `worker.py`, extracts the credentials, and sends them to a simulated attacker C2 server at `https://localhost:8443`.
- `run_env.sh`: A shell script that simulates the environment by running `monitor.py` in the background and then executing `processor.py`.

Your task is divided into three phases: Interception, Extraction, and Remediation.

**Phase 1: Interception (TLS & Server Setup)**
1. The attacker's script exfiltrates data via HTTPS to `localhost` on port `8443`. Generate a self-signed RSA TLS/SSL certificate and private key (unencrypted) in `/home/user/investigation/`. Name them `cert.pem` and `key.pem`. 
2. Write a Python HTTPS interceptor script in `/home/user/investigation/interceptor.py` that listens on `localhost:8443` using your generated certificate. 
3. The interceptor must be able to accept connections and print the raw HTTP request headers it receives. 

**Phase 2: Extraction (Payload Analysis)**
1. Start your interceptor script.
2. In another terminal, run `/home/user/investigation/run_env.sh` to trigger the leak.
3. Analyze the HTTP request received by your interceptor. The attacker hides the stolen credentials in the HTTP `Cookie` header in a base64-encoded format (look for a specific cookie name resembling a session identifier).
4. Decode the stolen payload.
5. Write the extracted credentials into `/home/user/investigation/stolen_creds.txt` in the exact format: `username:password`.

**Phase 3: Remediation (Process Isolation & Secure Coding)**
Passing secrets via command-line arguments is insecure because they are globally visible in `/proc/<pid>/cmdline`.
1. Modify `/home/user/investigation/processor.py` to no longer pass credentials as command-line arguments to `worker.py`. Instead, inject them into the subprocess's environment variables as `DB_USER` and `DB_PASS`.
2. Modify `/home/user/investigation/worker.py` to read `DB_USER` and `DB_PASS` exclusively from its environment variables. Remove any command-line argument parsing for the credentials.
3. Ensure that running `run_env.sh` again does not result in `monitor.py` successfully capturing the credentials.

Ensure your remediated code is syntactically correct and functional. Do not change the file paths or the names of the required output files.