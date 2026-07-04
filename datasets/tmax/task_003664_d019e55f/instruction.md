You are a network security engineer investigating a recent intrusion attempt on a custom data processing service running on port 7777. You have been provided with a packet capture of the incident. Your task involves analyzing the traffic, reverse-engineering the exploit payload, crafting a proof-of-concept exploit, writing a firewall rule to block the attacker, and hardening the server's SSH configuration to prevent fallback attacks.

Follow these steps precisely:

**Phase 1: Traffic Inspection (Data Processing)**
1. Analyze the packet capture located at `/home/user/capture.pcap`. The capture contains a TCP connection to port 7777.
2. Identify the IP address of the attacker (the client sending data to port 7777). Write this IP address to `/home/user/attacker_ip.txt`.
3. Extract the TCP data payload sent by the attacker. The payload is a simple command string encoded with a single-byte XOR cipher. You must determine the original command and the XOR key used (Hint: The original command is exactly 6 characters long and is a common Linux enumeration command).

**Phase 2: Exploit Crafting**
1. Write a Python script at `/home/user/craft_exploit.py`.
2. This script must encode the command `cat /etc/passwd` using the EXACT same single-byte XOR key discovered in Phase 1.
3. The script must output the encoded payload as raw bytes to a file named `/home/user/new_payload.bin`.

**Phase 3: Firewall Configuration**
1. Since you do not have root privileges to apply firewall rules directly, write a bash script at `/home/user/block_attacker.sh`.
2. The script should contain the exact `iptables` command needed to append (`-A`) a rule to the `INPUT` chain that drops (`DROP`) all incoming TCP traffic from the attacker's IP address (discovered in Phase 1) destined for local port 7777. Do not use `sudo` in the script.

**Phase 4: SSH Hardening and Key Management**
The attacker might try to pivot to SSH.
1. Generate an Ed25519 SSH key pair. Save the private key to `/home/user/admin_key` with no passphrase.
2. A default SSH configuration file exists at `/home/user/base_sshd_config`. Read it and create a new hardened version at `/home/user/hardened_sshd_config`.
3. In the hardened config, ensure the following settings are explicitly set (modify existing or add if missing):
   - Disable password authentication.
   - Disable root login completely.
   - Disable X11 forwarding.
   - Set the protocol version strictly to 2 (if not already implicitly the only protocol, add `Protocol 2`).

Ensure all files are created exactly at the specified paths. You may install standard Python packages (like `scapy`) using `pip` if needed.