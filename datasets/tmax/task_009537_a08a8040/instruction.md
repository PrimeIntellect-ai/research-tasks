You are an incident responder and forensics analyst investigating a compromised Linux host. You have isolated a suspicious binary and an encrypted payload. Your objective is to reverse engineer the malware, recover the stolen credentials, block the attacker's infrastructure, and secure the SSH configuration.

You must complete the following phases:

**Phase 1: Reverse Engineering & Analysis**
An unknown C++ binary is located at `/home/user/evidence/stealer.bin`. 
Analyze the binary to extract two critical pieces of information:
1. The IPv4 address used for data exfiltration (it is stored in the binary prefixed with `EXFIL_IP:`).
2. A single-byte XOR key used to encrypt the payload (stored in the binary prefixed with `XOR_KEY:` in hex format, e.g., `XOR_KEY:0xAA`).

**Phase 2: Cryptographic Recovery (C++)**
The attacker successfully gathered credentials before the process was killed, storing them in `/home/user/evidence/payload.enc`. 
Write a C++ program at `/home/user/decoder.cpp`. Your program must:
1. Compile successfully using `g++ /home/user/decoder.cpp -o /home/user/decoder`.
2. Accept exactly one command-line argument: the path to the encrypted payload file.
3. Read the file byte-by-byte.
4. Decrypt the contents using the XOR key you extracted in Phase 1.
5. Output the decrypted plaintext exactly as it is to a file named `/home/user/recovered.txt`.

**Phase 3: Network Policy Enforcement**
Create a bash script at `/home/user/block_ip.sh` to prevent further exfiltration.
The script must contain exactly one `iptables` command that appends a rule to the `OUTPUT` chain to `DROP` all traffic destined for the exfiltration IP address you found in Phase 1. 

**Phase 4: SSH Hardening**
The attacker left a backdoor in `/home/user/.ssh/authorized_keys`. 
1. Inspect the file and remove the SSH key associated with the attacker (its comment is `attacker@exfil-server`). Leave all other legitimate keys intact.
2. Ensure the `/home/user/.ssh/authorized_keys` file has the correct secure permissions (read and write for the user only, no permissions for group or others).

Ensure all requested files (`/home/user/decoder.cpp`, `/home/user/recovered.txt`, `/home/user/block_ip.sh`, and the modified `authorized_keys`) exist in the exact locations specified.