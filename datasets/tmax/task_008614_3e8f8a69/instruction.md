You are a forensics analyst recovering evidence from a compromised Linux host. The attacker left behind a trace of obfuscated payloads and a key-generation binary.

Here is what you know:
1. **The Key Generator**: There is a compiled ELF binary at `/home/user/get_key`. It requires a 4-digit numeric PIN as a command-line argument. Only one specific 4-digit PIN will cause the binary to print the correct encryption key and exit with a status code of 0.
2. **The Logs**: The file `/home/user/syslog` contains various noisy system logs. Hidden among them are lines with the exact phrase `Malicious Payload: ` followed by a base64-encoded string.
3. **The Encryption**: The base64 string, once decoded, is an XOR-encrypted payload. The XOR key is the string output by the `/home/user/get_key` binary when provided with the correct PIN. The XOR encryption wraps the key cyclically.
4. **The Evidence**: The decrypted payloads contain sensitive operational data, including IP addresses.

Your task is to:
1. Reverse engineer or brute-force the `/home/user/get_key` binary to find the correct 4-digit PIN and retrieve the string key.
2. Parse `/home/user/syslog` to extract the base64 payloads.
3. Decode and decrypt the payloads using the discovered key.
4. Redact *all* IPv4 addresses in the decrypted plaintext, replacing them exactly with the string `[REDACTED]`.
5. Save the redacted plaintexts to `/home/user/recovered_evidence.txt`, with each payload on a new line, preserving the order in which they appeared in the log file.

Use Bash to coordinate your workflow (you may write short helper scripts in Python/Perl for the XOR operation if needed). Do not leave unredacted IPs anywhere in the final output file.