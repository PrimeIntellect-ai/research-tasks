You are a compliance analyst investigating a potential web security breach. You have been provided with an encrypted archive of web access logs and a network firewall policy definition. Your goal is to decrypt the logs, verify their integrity, and analyze them against the firewall rules to generate an audit trail of policy violations.

All necessary files are located in `/home/user/audit_task/`.

**Step 1: File Integrity Verification**
Verify the SHA-256 checksum of the encrypted log archive `/home/user/audit_task/audit.enc` against the hash provided in `/home/user/audit_task/checksum.txt`. 

**Step 2: Cryptanalysis & Decryption**
The `audit.enc` file is an encrypted gzip archive (`.tar.gz`) containing the web logs. The encryption used is a weak repeating-key XOR cipher with a 4-byte (32-bit) key. 
Since you know the plaintext file is a standard gzip archive, you can perform a known-plaintext attack to recover the 4-byte key using the standard gzip magic bytes (`1F 8B 08 00`).
Once you have recovered the 4-byte key, decrypt the entire `audit.enc` file to recover the original `audit.tar.gz`, and extract its contents.

**Step 3: Web Security Audit**
The extracted archive contains a file named `access.log` (standard Apache/Nginx combined log format). 
You also have `/home/user/audit_task/policy.json`, which defines the firewall rules that *should* have been enforced by the network edge.
Analyze `access.log` to find any IP addresses that successfully accessed the server (HTTP status code 200) but violated the firewall policy. 
A request violates the policy if:
1. The source IP is NOT within any of the CIDR blocks listed in `allowed_subnets`.
2. OR the source IP is explicitly listed in `explicit_blocks`.

**Step 4: Report Generation**
Create a final report at `/home/user/report.json` containing the recovered XOR encryption key and the list of unique IP addresses that violated the firewall policy. The JSON must exactly match the following structure:

```json
{
  "encryption_key_hex": "A1B2C3D4", 
  "policy_violations": [
    "1.2.3.4",
    "5.6.7.8"
  ]
}
```
*Note: `encryption_key_hex` should be a capitalized 8-character hex string representing the 4-byte key.*