You are a forensics analyst responding to a compromised Linux host. The attacker exfiltrated sensitive data and left behind a few traces in the `/home/user/evidence/` directory. 

Your objective is to recover the stolen data, identify the attacker's exfiltration port, and document your findings.

Here is what we know:
1. **Firewall Modification**: The attacker modified the firewall to allow inbound connections from their IP address (`198.51.100.42`). A dump of the firewall rules is located at `/home/user/evidence/iptables_dump.txt`. Find the destination TCP port that was opened for this specific IP.
2. **Encrypted Exfiltration**: The attacker bundled a stolen TLS certificate into a password-protected ZIP archive located at `/home/user/evidence/exfil.zip`. We have intelligence indicating the password is exactly a 4-digit numeric PIN (e.g., 0000 to 9999).
3. **Stolen Certificate**: Once you crack the ZIP archive and extract the file (`server.crt`), analyze the TLS certificate to determine its Subject Common Name (CN).

You must write a Python script to brute-force the ZIP archive, extract the certificate, and parse it. You may also use standard command-line tools.

Create a final report at `/home/user/report.txt` with exactly the following format:
```
Attacker Port: <port_number>
ZIP Password: <4_digit_pin>
Certificate CN: <common_name>
```

Replace `<port_number>`, `<4_digit_pin>`, and `<common_name>` with the actual values you discover. Do not include any other text in the file.