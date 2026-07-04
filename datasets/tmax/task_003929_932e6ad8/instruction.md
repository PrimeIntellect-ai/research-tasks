You are an incident responder investigating a compromised server. You have discovered that the attacker is communicating with a backdoor via a specialized HTTP cookie containing an encoded binary payload.

A captured raw HTTP request from the attacker has been saved to `/home/user/incident_log.txt`. 

Your task is to write and execute a Rust program (at `/home/user/analyzer.rs`, compiled to `/home/user/analyzer`) that performs the following automated analysis and mitigation generation:

1. **HTTP Header and Cookie Inspection**: Read `/home/user/incident_log.txt` and parse it to extract the value of the `auth_token` cookie.
2. **Payload Decoding**: The cookie value is Base64 encoded. Decode it into raw bytes.
3. **Binary Format & ELF Analysis**: The decoded payload is an 8-byte custom binary struct. Validate that the first 4 bytes match the standard ELF magic number (`0x7F 'E' 'L' 'F'`). If they do not match, the program should exit with an error.
4. **IP Extraction**: If the magic bytes match, interpret the remaining 4 bytes as an IPv4 address (in network byte order / big-endian) representing the attacker's Command & Control (C2) server.
5. **Firewall Policy Configuration**: Based on the extracted IP, generate a bash script at `/home/user/mitigation.sh` that contains the exact `iptables` command to drop all inbound traffic from that IP. The file must start with `#!/bin/bash` and contain:
   `iptables -A INPUT -s <EXTRACTED_IP> -j DROP`
6. **Content Security Policy Enforcement**: To prevent further Cross-Site Scripting (XSS) based exfiltration on the affected endpoint, your Rust program must also create a file at `/home/user/csp_header.txt` containing exactly this strict CSP header line:
   `Content-Security-Policy: default-src 'none';`

Ensure `/home/user/mitigation.sh` is executable. You do not need to run the mitigation script, only generate it.