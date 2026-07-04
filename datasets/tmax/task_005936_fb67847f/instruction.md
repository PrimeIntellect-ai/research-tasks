You are a forensics analyst investigating a compromised Linux host. You have recovered a malicious C++ data exfiltration program and an encrypted data dump. Your objective is to safely reverse-engineer the exfiltration process, patch the malware so it doesn't crash, intercept the data locally using TLS, and redact the sensitive information.

All files are located in `/home/user/forensics/`.

Step 1: Vulnerability Analysis & C++ Patching
Review the source code of the recovered malware at `/home/user/forensics/exfil_malware.cpp`. It contains a classic buffer overflow vulnerability in the `parse_and_send` function where it copies decrypted data into a fixed-size buffer. 
- Fix the vulnerability in the C++ code (e.g., by using `strncpy` or `std::string` safely) so it can process payloads larger than 64 bytes without crashing.
- Compile the fixed code to `/home/user/forensics/malware_fixed` (use `g++ -o malware_fixed exfil_malware.cpp -lssl -lcrypto`).

Step 2: TLS Certificate Management
The malware is hardcoded to connect to a C2 server via TLS on `127.0.0.1` port `8443`.
- Generate a self-signed RSA-2048 certificate (`c2_cert.pem`) and private key (`c2_key.pem`) in the forensics directory.

Step 3: Process Isolation & Interception
You must intercept the data safely.
- Start a local TLS listener on port `8443` using `openssl s_server` with your generated certificate and key. Route its output to `/home/user/forensics/intercepted.raw`.
- To prevent the malware from accidentally communicating with any external network, you must run it in an isolated network namespace. Create a bash script at `/home/user/forensics/run_isolated.sh` that uses `unshare -r -n` to create a new network namespace, brings up the loopback interface (`ip link set lo up`), and executes `./malware_fixed`. 
- Run your script so the malware processes `/home/user/forensics/dump.bin` and sends the data to your local listener.

Step 4: Sensitive Data Redaction
The intercepted data in `intercepted.raw` contains stolen user records, including Social Security Numbers in the format `XXX-XX-XXXX` (where X is a digit).
- Write a command or script to read `intercepted.raw` and redact all SSNs by replacing them exactly with the string `REDACTED-SSN`.
- Save the final redacted output to `/home/user/forensics/final_evidence.log`.

Ensure all requested files are created exactly at the specified paths.