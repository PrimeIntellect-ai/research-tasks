You are a forensics analyst investigating a compromised Linux host. The attacker left behind an evidence directory at `/home/user/evidence` containing scripts used for maintaining persistence via forged authentication tokens, as well as logs from their automated vulnerability scanning.

Your objective is to recover the attacker's forging mechanism, identify the privilege escalation vector, and write an automated bash script to test the authentication flow.

Perform the following tasks:

1. **Token Generation Analysis:**
   The attacker left a script at `/home/user/evidence/forge_token.sh`. It generates authentication tokens for arbitrary users. Analyze this script and the surrounding directory to find the cryptographic secret used to sign the tokens. 
   Once you understand the generation logic, manually generate a valid token for the username `forensic_admin` with the exact timestamp `1715000000`. Save ONLY the final 64-character SHA256 token string into `/home/user/recovered_token.txt`.

2. **Privilege Escalation Auditing:**
   The file `/home/user/evidence/privesc_scan.log` contains the output of the attacker's automated vulnerability scanning for SUID binaries. Identify the anomalous custom binary in this list that the attacker most likely exploited to gain root privileges (it is not a standard Linux utility like `passwd`, `sudo`, or `su`).
   Write the absolute path of this binary into `/home/user/exploited_binary.txt`.

3. **Authentication Flow Testing (Bash Scripting):**
   The file `/home/user/evidence/auth_service_mock.sh` is a mock of the compromised service. It takes a username, a timestamp, and a token as arguments, and validates them: `./auth_service_mock.sh <username> <timestamp> <token>`.
   Write a new Bash script at `/home/user/test_auth_flow.sh` that:
   - Takes exactly two arguments: a username and a timestamp.
   - Automatically generates the correct token using the attacker's logic and the discovered secret.
   - Calls `/home/user/evidence/auth_service_mock.sh` with the provided username, timestamp, and generated token.
   - Forwards the exit code of `auth_service_mock.sh`.
   Make sure `/home/user/test_auth_flow.sh` is executable.

Ensure all output files are placed exactly as requested.