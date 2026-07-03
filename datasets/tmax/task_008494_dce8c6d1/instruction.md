You are a forensics analyst responding to a suspected compromise. A memory forensics tool has dumped the `/proc` directory state of a suspicious process into `/home/user/evidence/proc_9999/`. 

The process appears to be a Python-based malware that leaked its Command and Control (C2) server configuration via its command-line arguments.

Your task:
1. Analyze the file `/home/user/evidence/proc_9999/cmdline`. This file contains the null-byte (`\0`) separated arguments passed to the malicious process.
2. Locate the `--c2-payload` argument. Its value is a Base64-encoded string representing the C2 server's `<IP>:<PORT>`.
3. Locate the `--verify` argument. Its value is the SHA-256 hash of the *decoded* C2 server string.
4. Write a Python script at `/home/user/extract_c2.py` that programmatically:
   - Reads the `cmdline` file.
   - Extracts and decodes the Base64 payload.
   - Computes the SHA-256 hash of the decoded payload and verifies it matches the `--verify` value.
   - If the hash matches, writes the decoded `<IP>:<PORT>` string to `/home/user/c2_address.txt`.
5. Once you have extracted the C2 address, create a shell script at `/home/user/firewall_block.sh` to prevent further communication. Since you do not have root access to apply the rule directly, simply write the rule into the file. The file must contain exactly one line with the following `iptables` command to drop all outbound TCP traffic to that specific IP and port:
   `iptables -A OUTPUT -d <IP> -p tcp --dport <PORT> -j DROP`

Execute your Python script to ensure `/home/user/c2_address.txt` is generated correctly.