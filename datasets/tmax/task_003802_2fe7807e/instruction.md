You are a forensics analyst investigating a compromised Linux web server. The attacker left behind a suspicious binary executable and an encrypted staging file containing exfiltrated data and command-and-control (C2) configurations.

Your objective is to recover the evidence by analyzing the binary, writing a custom decryption tool in Rust, and extracting specific indicators of compromise (IoCs) from the decrypted payload.

Here are the details of your investigation:
1. **Evidence Location:** You will find the forensics data in `/home/user/forensics/`. It contains two files: `malware_agent` (an ELF binary) and `exfiltrated.enc` (the encrypted payload).
2. **Binary Analysis:** The attacker hardcoded the encryption key inside the `malware_agent` binary. Extract this key. It is a 16-byte key stored in a custom ELF section named `.c2_key`.
3. **Decryption (Rust):** Create a new Rust project at `/home/user/decryptor`. Write a Rust program that reads `/home/user/forensics/exfiltrated.enc` and decrypts it using a repeating multi-byte XOR cipher with the 16-byte key you extracted. Save the decrypted file as `/home/user/forensics/exfiltrated.dec`. (The file is small, so reading it entirely into memory is fine).
4. **IoC Extraction:** The decrypted file is a plaintext log. You need to analyze it to extract two things:
   - **Forged TLS Certificate:** The file contains a complete X.509 certificate in PEM format used by the attacker's C2 server. Extract this certificate and calculate its SHA-256 fingerprint.
   - **Injection Payload:** The file logs the initial SQL injection payload used to compromise the system. It contains the string `UNION SELECT`. Extract the exact, complete line containing this payload.

**Deliverable:**
Generate a final JSON report at `/home/user/forensics_report.json` containing the exact following keys:
- `"c2_key_hex"`: The 16-byte encryption key represented as a 32-character lowercase hex string.
- `"cert_fingerprint_sha256"`: The SHA-256 fingerprint of the forged TLS certificate, formatted exactly as output by OpenSSL (e.g., `DE:AD:BE:EF:...`).
- `"sqli_payload"`: The exact, complete line from the log containing the SQL injection string.

Ensure your Rust code compiles and runs using the standard `cargo` toolchain available on the system.