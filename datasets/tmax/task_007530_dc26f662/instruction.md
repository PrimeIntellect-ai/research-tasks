You are acting as a forensics analyst investigating a compromised Linux host. The attacker left behind several artifacts in the directory `/home/user/evidence/`. You need to build a custom forensic triage tool in **Rust** to analyze these artifacts, decode the attacker's payload, and audit the local privilege escalation path they attempted to use.

Your task is to create a Rust project in `/home/user/forensic_tool` that performs the following three phases, outputting the final findings to a JSON file at `/home/user/report.json`.

**Phase 1: Privilege Escalation Auditing**
The attacker attempted to use a misconfigured SUID binary in the `/home/user/evidence/bin/` directory. 
Your Rust program must scan the `/home/user/evidence/bin/` directory and identify all files that have the SUID bit set (ignoring standard system paths, just check this specific directory).

**Phase 2: TLS Certificate Analysis**
The attacker left behind a rogue TLS certificate at `/home/user/evidence/attacker.crt` used for their C2 server. 
Your Rust program must parse this X.509 certificate and extract the "Common Name" (CN) from the Subject field.

**Phase 3: Payload Decoding**
The attacker left an encrypted payload file at `/home/user/evidence/payload.enc`. 
The payload is encoded using a custom method:
1. The file content is a raw hex-encoded string.
2. Once hex-decoded into bytes, the bytes are XOR-encrypted.
3. The XOR key is the Common Name (CN) extracted from the certificate in Phase 2, repeated cyclically. 
   (e.g., if the CN is "abc", the first byte is XOR'd with 'a', the second with 'b', the third with 'c', the fourth with 'a', etc.)
Your Rust program must hex-decode the file, decrypt it using the cyclic XOR key, and convert the result to a UTF-8 string.

**Final Output Requirement:**
Your Rust program must generate a file exactly at `/home/user/report.json` with the following structure:
```json
{
  "suid_binaries": ["binary_name1", "binary_name2"],
  "cert_common_name": "extracted_cn_here",
  "decoded_payload": "decoded_string_here"
}
```
*Note: The `suid_binaries` list should only contain the base filenames (not full paths), sorted alphabetically.*

Ensure your Rust program manages its dependencies (like `x509-parser` or `hex`, if you choose to use them) properly via `Cargo.toml`. You must compile and run the program to generate the `report.json` file.