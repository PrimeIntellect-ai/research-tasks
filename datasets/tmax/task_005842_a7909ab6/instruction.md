You are acting as a penetration tester auditing a mock internal service configuration. You have been provided with several configuration files and scripts from the target environment. Your objective is to analyze these artifacts, uncover vulnerabilities, and demonstrate exploitation.

Perform the following steps:

1. **Firewall Policy Analysis**
   You have a dumped firewall configuration file located at `/home/user/firewall.txt`. Analyze the rules to find the specific TCP port that explicitly allows incoming connections ONLY from the IP address `203.0.113.50`. Write this port number on **line 1** of a new file called `/home/user/findings.log`.

2. **TLS/SSL Certificate Management**
   The service uses a self-signed certificate located at `/home/user/server.pem`. Extract the SHA-1 fingerprint of this certificate. Write the fingerprint (in standard hexadecimal format, e.g., `AA:BB:CC...`) on **line 2** of `/home/user/findings.log`.

3. **Cryptanalysis and Checksum Verification**
   The application's authentication module is stored in `/home/user/crypto_auth.py`. This Python file contains a function `verify_token(token, username)` which implements a custom, highly vulnerable cryptographic verification scheme to validate user sessions.
   Review the logic in `/home/user/crypto_auth.py` and write a Python script located at `/home/user/exploit.py`. Your script must dynamically generate a valid token for the username `admin_root_system` and print ONLY the valid token to standard output.

Constraints:
- Do not modify `/home/user/firewall.txt`, `/home/user/server.pem`, or `/home/user/crypto_auth.py`.
- Your `/home/user/exploit.py` must run successfully with Python 3 and output exactly the generated token string.
- `/home/user/findings.log` must contain exactly two lines as specified.