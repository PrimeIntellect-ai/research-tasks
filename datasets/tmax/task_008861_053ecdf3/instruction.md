You are a forensics analyst responding to a compromised Linux host. You have isolated a set of artifacts left behind by the attacker in the directory `/home/user/evidence/`. 

Your goal is to analyze the malicious payload, block its communication, and recover the stolen data.

**Phase 1: Binary Analysis**
There is a suspicious executable located at `/home/user/evidence/beacon`. The attacker compiled this binary to communicate with their Command and Control (C2) server. 
Using standard Linux CLI tools (e.g., `strings`, `objdump`, `grep`), analyze the binary to extract the hardcoded C2 IPv4 address and the TCP destination port it attempts to connect to. The IP address string is immediately prefixed with `C2_HOST=` and the port with `C2_PORT=` in the binary's read-only data section.

**Phase 2: Network Policy Configuration**
Once you have extracted the IP and port, create a Bash script at `/home/user/firewall_block.sh`. 
This script must contain exactly one `iptables` command to append (`-A`) a rule to the `OUTPUT` chain that `DROP`s all outbound `tcp` traffic destined for the extracted C2 IP address (`-d`) and specific destination port (`--dport`). 
Ensure the script is executable.

**Phase 3: Password Cracking and Evidence Recovery**
The attacker also encrypted the stolen files into a single archive before exfiltration, located at `/home/user/evidence/stolen_data.enc`. 
Through previous intelligence, we know the encryption password is exactly a 4-digit numeric PIN (e.g., 0000 to 9999). 
The file was encrypted using standard OpenSSL with the following parameters: `aes-256-cbc` and `-pbkdf2`.

Write and execute a Bash script to brute-force the 4-digit PIN. Use the `openssl` command to attempt decryption. 
When successfully decrypted, save the output to `/home/user/recovered_data.txt`. 
(Hint: Use a `for` loop in Bash and check the exit code of `openssl enc -d -aes-256-cbc -pbkdf2 -in /home/user/evidence/stolen_data.enc -out /home/user/recovered_data.txt -pass pass:$PIN`).

**Success Criteria:**
1. `/home/user/firewall_block.sh` exists, is executable, and contains the correct `iptables` command.
2. `/home/user/recovered_data.txt` contains the successfully decrypted plaintext.