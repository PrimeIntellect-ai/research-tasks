You are acting as a security auditor evaluating an internal system. The system consists of three components located in `/app/`:
1. An Nginx reverse proxy (supposed to run on port 8080).
2. A Flask authentication service (running on port 5000).
3. A legacy permission-checking daemon that relies on a stripped ELF binary.

You have three main objectives to complete your audit and remediate the immediate issues:

**Objective 1: Multi-Service Configuration**
The services are currently failing to communicate securely. 
- You need to configure Nginx (using the config template at `/app/nginx/nginx.conf`) to proxy requests from `http://localhost:8080/auth/` to the Flask service at `http://127.0.0.1:5000/`.
- The Flask service generates JWT tokens but is currently using a hardcoded weak secret. Modify the Flask configuration file `/app/flask/config.py` to read the secret from the environment variable `AUTH_SECRET`. 
- Start the Nginx and Flask services in the background.

**Objective 2: Password Cracking for Admin Access**
You found an exposed password hash in `/app/data/admin_hash.txt` (MD5 hash format). To perform a full end-to-end test, you must crack this hash. The password is a 5-character lowercase English word. Once cracked, write the plaintext password to `/home/user/admin_password.txt`.

**Objective 3: Binary Analysis and Implementation (Equivalence Testing)**
The legacy permission checker is a stripped ELF binary located at `/app/bin/legacy_perm_check`. It takes exactly two positional arguments: a 16-character hexadecimal string (`token`) and a resource name (`resource_id`), e.g., `/app/bin/legacy_perm_check 1a2b3c4d5e6f7a8b users`. 
It outputs either `ALLOW` or `DENY` to stdout. 

Because the binary has memory corruption vulnerabilities, your task is to black-box or reverse-engineer its logic and write a pure Python equivalent. 
Write your implementation to `/home/user/perm_check.py`. 
Your script must take the exact same command-line arguments and produce the exact same standard output as the binary for *any* valid input format. Automated verification will fuzz your script against a hidden reference oracle with thousands of random inputs to ensure bit-exact equivalence.

*Requirements for `/home/user/perm_check.py`:*
- Must use `#!/usr/bin/env python3` as the shebang.
- Must accept two arguments (sys.argv[1] and sys.argv[2]).
- Must print exactly `ALLOW` or `DENY` (followed by a newline).