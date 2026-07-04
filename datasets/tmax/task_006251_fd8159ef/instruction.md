You are a forensics analyst responding to a breach on a compromised Linux host. The attacker exploited an open redirect vulnerability in the web server's login flow to hijack an administrator session, established a backdoor, and exfiltrated sensitive database records.

Your goal is to retrace the attacker's steps, decrypt the exfiltrated data, crack the archive, and prepare a sanitized evidence file for legal review. You must use **Go** for any custom programming tasks. 

Perform the following tasks:

1. **Firewall Policy Analysis**
The system administrator captured the host's iptables rules just after the breach. The dump is located at `/home/user/forensics/fw_dump.txt`. The attacker inserted a custom rule to allow outbound communication to their Command and Control (C2) server specifically on port `1337`. 
Analyze the firewall dump, extract the C2 IP address, and save it to a file named `/home/user/c2_ip.txt`.

2. **Payload Decoding and Cryptanalysis**
The attacker left behind an encrypted exfiltration archive at `/home/user/forensics/payload.enc`. 
- The file is hex-encoded.
- Once hex-decoded, the binary data is encrypted using a repeating multi-byte XOR cipher.
- Forensics indicate the XOR key is exactly 4 bytes long and begins with the ASCII characters `C2`. The remaining 2 bytes are printable ASCII characters.
Write a Go program to brute-force the remaining 2 bytes of the XOR key. You know the underlying plaintext is a standard ZIP archive (Hint: ZIP files always start with the magic bytes `PK\x03\x04`). Once your Go program finds the correct key, have it decrypt the entire file and save the output to `/home/user/forensics/payload.zip`.

3. **Password Cracking**
The recovered `payload.zip` is password-protected. The attacker is known to use weak passwords found in standard dictionaries. We have provided a dictionary at `/home/user/wordlist.txt`. 
Crack the password of the ZIP file and extract its contents to `/home/user/forensics/`. You should recover a file named `exfiltrated.json`. (You may use bash tools or Go for this step).

4. **Sensitive Data Redaction**
The `exfiltrated.json` file contains an array of user records. Each record is a JSON object with the fields: `id`, `username`, `email`, and `credit_card`.
Write a Go program to parse this JSON file, redact the sensitive payment information by replacing the exact value of every `credit_card` field with the literal string `[REDACTED]`, and write the resulting JSON array to `/home/user/evidence_clean.json`. Ensure the output is valid JSON.

Constraints:
- Do not use root/sudo.
- Use Go as your primary programming language for the cryptographic and redaction steps.
- Make sure all output files are placed exactly at the paths requested.