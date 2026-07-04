You are a forensics analyst investigating a compromised Linux host. You have been provided with a directory of evidence at `/home/user/evidence/` containing three files:

1. `/home/user/evidence/auth_logs.json`: A log of authentication attempts in JSON Lines format. Each line is a JSON object with the keys: `timestamp` (integer UNIX epoch), `ip` (string), `username` (string), and `status` (string, either "failed" or "success"). 
2. `/home/user/evidence/suspicious.elf`: A malicious ELF executable discovered on the system.
3. `/home/user/evidence/payload.bin`: An encrypted binary payload exfiltrated by the attacker.

Your objective is to correlate the logs, analyze the binary, decrypt the payload, and generate a final forensics report. You must use Python to perform your analysis. 

Perform the following steps:

**Phase 1: Log Parsing and Authentication Analysis**
Analyze `auth_logs.json` to identify the attacker's IP address. The attacker's IP is uniquely identifiable by their authentication flow: they are the *only* IP address that has exactly 15 consecutive "failed" login attempts within a 60-second window, immediately followed by a "success" attempt.

**Phase 2: ELF Analysis**
The attacker hid an encryption key inside the `suspicious.elf` binary. Use Python or standard Linux binary analysis tools to extract the raw bytes from a custom ELF section named `.malconf`. This section contains exactly 8 bytes which serve as the decryption key.

**Phase 3: Payload Decryption**
The file `payload.bin` is encrypted. The encryption is a repeating multi-byte XOR using the 8-byte key you extracted from the `.malconf` section of the ELF binary. Write a Python script to decrypt the payload. The decrypted payload contains a plaintext ASCII flag.

**Phase 4: Reporting**
Create a JSON-formatted forensics report at `/home/user/report.json` with the following exact structure:
```json
{
  "attacker_ip": "<identified_ip_address>",
  "extracted_key_hex": "<the_8_byte_key_as_a_lowercase_hex_string>",
  "decrypted_flag": "<the_decrypted_flag_string>"
}
```

Ensure your output file strictly adheres to this format, as it will be programmatically validated.