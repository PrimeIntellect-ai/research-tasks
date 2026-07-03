You are a forensics analyst investigating a compromised unprivileged Linux server. We suspect an attacker left behind a compiled binary that exfiltrates data and altered local files to maintain persistence. Your goal is to reverse engineer the binary's network indicators, verify the integrity of local files, and extract the stolen data from intercepted traffic logs.

You are provided with the following in `/home/user/`:
1. `malware_bin`: An unknown compiled ELF binary left by the attacker.
2. `evidence/`: A directory containing various system configuration backups.
3. `known_hashes.txt`: A text file containing the original SHA-256 hashes of the files in the `evidence/` directory, formatted as `<hash>  <filename>`.
4. `traffic.log`: A JSON-lines log file containing intercepted HTTP requests.

Your task consists of three phases. You must write a Go program at `/home/user/forensics.go` to automate the extraction and verification.

**Phase 1: Binary & ELF Analysis**
Analyze `malware_bin` (using static analysis tools like `strings`, `readelf`, or `objdump`). Identify:
- The Command and Control (C2) IP address and port it attempts to connect to.
- The specific custom HTTP Header name it uses to pass the exfiltrated data.
- The hardcoded HTTP Cookie value used for C2 authentication.

**Phase 2: File Integrity Verification**
Your Go program (`forensics.go`) must scan the `/home/user/evidence/` directory, compute the SHA-256 hash of each file, and compare it against `/home/user/known_hashes.txt`. Identify the exact filename of the single modified file (the one whose hash no longer matches).

**Phase 3: HTTP Inspection & Extraction**
Your Go program must read `/home/user/traffic.log`. Using the C2 IP, port, and Cookie value discovered in Phase 1, filter the logs to find the single malicious exfiltration request. Extract the exfiltrated payload from the custom HTTP header (the payload is base64 encoded; your Go script must decode it to plaintext).

**Output format:**
Your Go program must write the results to `/home/user/forensics_report.json` in the exact following format:
```json
{
  "c2_ip": "x.x.x.x",
  "c2_port": 1234,
  "auth_cookie": "cookie_value_here",
  "custom_header_name": "Header-Name-Here",
  "compromised_file": "filename.ext",
  "decoded_payload": "plaintext_payload_here"
}
```

Write, compile, and execute your Go program to generate the report. Ensure all fields are accurately populated.