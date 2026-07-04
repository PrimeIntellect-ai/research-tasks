You are a network security engineer investigating a recent intrusion. You have been provided with an HTTP traffic log file located at `/home/user/traffic_capture.json`. The log contains an array of JSON objects representing HTTP requests.

The attacker successfully bypassed authentication and dropped a malicious payload. We suspect they exploited a vulnerability in our JWT implementation.

Your objective is to write a Python script (e.g., `/home/user/analyze.py`) to perform a multi-phase analysis of this traffic and extract the attacker's configuration.

Perform the following steps programmatically:
1. **Identify the malicious request:** Parse the traffic log and locate the single request that successfully bypassed authentication by forging a JWT with an `alg` (algorithm) header set to `none` (case-insensitive) and a payload claiming the `"role"` is `"admin"`.
2. **Extract the payload:** Retrieve the `data` field from this specific HTTP request. The data contains an SQL injection string, inside of which is a Base64-encoded string representing the dropped malware payload. Extract this Base64 string.
3. **Decrypt the malware:** Decode the Base64 string. The resulting bytes are obfuscated using a single-byte XOR cipher. You must brute-force the 1-byte XOR key (0x00 to 0xFF) by looking for the standard ELF magic bytes (`\x7fELF`) at the beginning of the decrypted output.
4. **Save the binary:** Once the correct key is found, save the decrypted ELF binary to `/home/user/malware.elf`.
5. **Binary Analysis:** Analyze the decrypted ELF binary (you may use Python tools, `lief`, or parse standard Linux binary utilities like `strings` or `readelf` via Python). The ELF contains a hardcoded command-and-control server address. Find the printable string that begins with `C2_SERVER=` and extract the URL/IP that follows it.
6. **Reporting:** Generate a final report in JSON format at `/home/user/report.json` with the exact following structure:
```json
{
  "malicious_jwt": "<the full exact JWT string from the Authorization header>",
  "xor_key_decimal": <the integer value of the discovered XOR key in decimal format>,
  "c2_server_address": "<the extracted C2 address, e.g., http://evil.com/api>"
}
```

Constraints:
- You must use Python to drive the analysis.
- The `traffic_capture.json` file is already present on the system.
- Ensure your output JSON is correctly formatted and uses the exact keys specified above.