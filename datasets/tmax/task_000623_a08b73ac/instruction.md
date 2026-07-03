As a penetration tester, you have been tasked with automating a local security audit using Rust. You must write a Rust program that audits local SSH keys for known vulnerabilities, performs a local port scan to locate a hidden vulnerable service, interacts with the service using encoded payloads, and verifies the response via cryptographic hashing.

Write your Rust project in `/home/user/audit_tool`. Your program must perform the following operations:

1. **SSH Key Auditing:**
   - Parse the file `/home/user/.ssh/authorized_keys`. Each line contains an SSH public key in the standard format: `<key_type> <base64_data> <comment>`.
   - Read the list of known compromised key hashes from `/home/user/compromised.txt`. This file contains one SHA256 hex digest per line.
   - For each key in `authorized_keys`, extract the `<base64_data>` part. Compute the SHA256 hex digest of this base64 string (hash the string directly as UTF-8 bytes). Identify any keys whose hashes match those in the compromised list.

2. **Service Auditing & Port Scanning:**
   - Scan local TCP ports in the range `8000` to `8010` (inclusive) on `127.0.0.1`. Exactly one port in this range will be open, hosting a mock vulnerable service.
   - Connect to the open port.
   - Send the payload `U0NBTl9DT01NQU5E\n` (this is the Base64 encoding of `SCAN_COMMAND` followed by a newline character).

3. **Payload Decoding & Verification:**
   - Read the response from the server (until a newline is encountered or the connection closes). The response is a Base64-encoded string.
   - Decode the Base64 response into raw bytes, and convert it to a UTF-8 string.
   - Compute the SHA256 hex digest of this decoded string (as UTF-8 bytes).

4. **Reporting:**
   - Write the final results to `/home/user/audit_report.json` in the exact format shown below:

```json
{
  "compromised_keys": [
    "COMPROMISED_SHA256_HEX_DIGEST"
  ],
  "open_port": 8005,
  "decoded_response": "DECODED_STRING_HERE",
  "response_hash": "SHA256_HEX_DIGEST_OF_DECODED_STRING"
}
```

Constraints:
- You must write and execute the Rust code to complete this task.
- The JSON output must be pretty-printed or minified, as long as the keys and values are strictly correct and match the specified names.
- Ensure the Rust program correctly manages dependencies (e.g., using `cargo add sha2 base64 serde_json` etc. as you see fit).
- Run your tool and ensure `/home/user/audit_report.json` is generated correctly.