You are an incident responder investigating a compromised Linux server. You have recovered an encrypted payload dropped by the attackers, located at `/home/user/evidence/payload.enc`. 

Through previous forensic analysis, you know the following about the payload and its encryption:
1. The file was encrypted using a repeating-key XOR cipher.
2. The XOR key is exactly 4 characters long and consists entirely of lowercase English letters (`a-z`).
3. The underlying decrypted file is a standard Linux ELF executable, meaning its first 4 bytes are the ELF magic number (`\x7FELF`).
4. Embedded within the decrypted ELF executable is the attacker's Command and Control (C2) configuration. It is preceded by the exact ASCII marker `C2_START`. Immediately following this 8-byte marker are 4 bytes representing the IPv4 address, followed by 2 bytes representing the TCP port in network byte order (big-endian).

Your tasks are:
1. Write a C program (e.g., at `/home/user/decryptor.c`) to brute-force the 4-character XOR key, decode the payload, and save the decrypted file to `/home/user/payload.bin`.
2. Analyze the decrypted `/home/user/payload.bin` to extract the C2 IP address and port.
3. Write the exact `iptables` command needed to block all outbound TCP traffic to this specific IP and port. Because you do not have root privileges to apply it, save the command as a single line in a text file at `/home/user/firewall_rule.txt`.

The format of the `iptables` command in `/home/user/firewall_rule.txt` must exactly match:
`iptables -A OUTPUT -d <IP> -p tcp --dport <PORT> -j DROP`
(Replace `<IP>` and `<PORT>` with the extracted values).

Ensure your final decrypted binary is correctly saved at `/home/user/payload.bin` and the firewall rule is written to `/home/user/firewall_rule.txt`.