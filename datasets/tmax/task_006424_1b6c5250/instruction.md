You are a DevSecOps engineer responsible for enforcing infrastructure security policies as code.

You need to write a Rust program that analyzes system logs for intrusions and audits local TLS certificates for expiration, then generates a firewall policy script to block threats and insecure services.

Please create a Rust project in `/home/user/policy_builder` and write a program that does the following:

1. **Intrusion Detection (Pattern Matching):**
   Read the Nginx access log located at `/home/user/access.log`.
   Identify any IP addresses that have attempted a SQL injection attack. For this task, an attack is defined as any log line containing the exact string `UNION SELECT`.
   Extract the IP address (the first space-separated field on the matching lines).

2. **TLS Certificate Auditing:**
   Audit all X.509 certificates located in the directory `/home/user/certs/`.
   The certificates are named following the pattern `port_<PORT_NUMBER>.pem` (e.g., `port_8081.pem`).
   Determine which certificates have expired (their "Not After" date is in the past compared to the current system time). You may shell out to OpenSSL from your Rust code or use a Rust crate to check this.

3. **Firewall Policy Generation:**
   Your Rust program must generate a bash script at `/home/user/enforce.sh` that contains `iptables` rules to drop traffic from the malicious IPs and to the ports with expired certificates.
   
   The output file `/home/user/enforce.sh` MUST follow this exact format:
   ```bash
   #!/bin/bash
   # IP Blocklist
   iptables -A INPUT -s <IP_1> -j DROP
   iptables -A INPUT -s <IP_2> -j DROP
   # Port Blocklist
   iptables -A INPUT -p tcp --dport <PORT_1> -j DROP
   iptables -A INPUT -p tcp --dport <PORT_2> -j DROP
   ```
   
   **Formatting Constraints:**
   - The IP drop rules must appear first, sorted lexicographically by the IP address string. Ensure each malicious IP is listed exactly once (deduplicate).
   - The Port drop rules must appear second, sorted numerically by the port number (lowest to highest). Ensure each port is listed exactly once.
   - Include the exact header comments `# IP Blocklist` and `# Port Blocklist` as shown above.
   
Execute your Rust program so that `/home/user/enforce.sh` is created, then make `/home/user/enforce.sh` executable (`chmod +x`).