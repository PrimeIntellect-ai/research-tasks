You are an incident responder investigating a recent breach on a web server. The attacker exploited a file upload handler susceptible to path traversal, bypassed file integrity checks, and established a persistent backdoor. You must perform the following tasks:

1. **Video Analysis**: A compromised jump host captured a screen recording of the attacker's terminal session during the breach. The video is located at `/app/breach_capture.mp4`. Extract the frames to determine the exact filename of the malicious ELF binary the attacker dropped (it appears prominently on screen around the 5-second mark).
2. **Binary & Integrity Analysis**: Locate this ELF file within the `/var/www/uploads/` directory (the attacker used path traversal to place it outside the normal `images` folder). Analyze the ELF binary to find the hardcoded fallback communication port (stored as a 16-bit integer in a section named `.bk_port`). Additionally, verify the integrity of the files in `/var/www/` against the manifest located at `/app/manifest.sha256`. Identify the single legitimate file whose file permission was maliciously altered to `0777`.
3. **TLS Certificate Management**: The attacker installed a rogue TLS certificate to intercept internal traffic. Parse the certificate at `/etc/ssl/certs/rogue.pem` and extract the Common Name (CN) of the Issuer.
4. **Path Sanitization Replication**: To help our security engineers build a precise WAF rule, you must write a Python script that exactly replicates the flawed path traversal sanitization logic used by the vulnerable upload handler. We have a compiled reference oracle of this broken logic at `/app/oracle_sanitizer`. Your script must be written to `/home/user/sanitizer.py`. It should read a raw file path from standard input, process it, and print the resulting (flawed) sanitized path to standard output. Your script will be tested against the oracle using random fuzzing to ensure bit-exact output equivalence.
5. **Reporting**: Compile your findings into a JSON report at `/home/user/investigation_report.json` with the following structure:
```json
{
  "dropped_elf_filename": "<filename from video>",
  "backdoor_port": <integer>,
  "altered_file": "<relative path of the file from /var/www/ with 0777 permissions>",
  "rogue_issuer_cn": "<Issuer CN>"
}
```