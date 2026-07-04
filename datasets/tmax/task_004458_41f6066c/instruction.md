You are acting as a forensics analyst investigating a compromised Linux host. The attacker exfiltrated sensitive data and left behind a malicious executable and a video artifact.

Your objective is to recover the attacker's TLS private key from the video, verify the malware's embedded certificate, and safely redact the exfiltrated sensitive data directly within the ELF binary without corrupting its structure.

**Step 1: Video Forensics**
You have been provided a video artifact at `/app/evidence.mp4`. The attacker used a visual covert channel to transmit a TLS private key. 
Extract the frames from this video. Certain frames contain QR codes. Decode these QR codes (you may use `zbarimg` and `ffmpeg`, which are pre-installed). The decoded text from the sequence of QR codes, when concatenated in chronological order, will form a PEM-encoded RSA private key.

**Step 2: Binary & Vulnerability Analysis**
Analyze the malicious ELF binary located at `/app/malware.elf`. 
The binary contains two custom ELF sections:
1. `.tls_cert`: Contains a PEM-encoded public TLS certificate.
2. `.exfil_data`: Contains raw, unencrypted text containing a mix of benign application logs, Command & Control (C2) URLs, and exfiltrated PII.

Using Go, write a tool at `/home/user/analyze.go` that:
- Parses the ELF binary.
- Reads the `.tls_cert` section and mathematically verifies that it matches the RSA private key recovered from the video.

**Step 3: Sensitive Data Redaction**
Extend your Go tool to redact sensitive information if (and only if) the certificate matches the recovered key.
In the `.exfil_data` section, locate all instances of:
- Credit Card Numbers: exactly matching the format `XXXX-XXXX-XXXX-XXXX` (where X is a digit).
- Email Addresses: standard format (e.g., `user@domain.com`).

Redact these instances by overwriting the characters with asterisks (`*`). For example, `1234-5678-9012-3456` becomes `*******************`. **Do not alter the length of the string, the section offsets, or any other data.** C2 URLs and system logs must remain completely intact.

**Output:**
Your Go program should output the patched, executable binary to `/home/user/sanitized.elf`.

**Evaluation:**
An automated metric script will evaluate `/home/user/sanitized.elf` to calculate the F1-score of correctly redacted bytes vs incorrectly redacted bytes. To pass, you must achieve an F1-score of >= 0.95.