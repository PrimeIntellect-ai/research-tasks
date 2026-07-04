You are a forensics analyst assigned to recover evidence from a compromised Linux host. The attacker left behind an obfuscated staging binary and a log file containing exfiltrated data disguised as HTTP traffic. 

Your objective is to extract the decryption key from the attacker's binary, locate the hidden data within the HTTP logs, write a C program to decode the data, and secure the recovered evidence.

Here are your specific tasks:

1. **Vulnerability Analysis & Exploit Crafting:**
   The attacker left a binary at `/home/user/attacker_bin`. You suspect this binary has a hidden function that prints the XOR encryption key used for exfiltration. The binary is known to be vulnerable to a classic buffer overflow (it reads from standard input). 
   - Analyze `/home/user/attacker_bin` (it is an unstripped 64-bit ELF executable).
   - Craft a binary payload to overwrite the instruction pointer and jump to the hidden `print_key` function.
   - Run the exploit against `/home/user/attacker_bin` to recover the 1-byte XOR key.

2. **HTTP Header Inspection:**
   The file `/home/user/exfil.log` contains captured HTTP requests. The attacker hid the exfiltrated data inside the HTTP cookies. Specifically, the data is stored as hex-encoded strings in the `Cookie: auth_token=` header across multiple HTTP requests.

3. **Data Processing (C Language):**
   Write a C program at `/home/user/decoder.c` that:
   - Reads `/home/user/exfil.log`.
   - Extracts all the hex-encoded strings from the `Cookie: auth_token=` headers.
   - Converts the hex strings back to raw bytes.
   - Decrypts the bytes by XORing them with the key you recovered in Step 1.
   - Concatenates the decrypted strings in the order they appear in the log.

4. **Evidence Preservation:**
   - Your C program (or a subsequent shell command) must write the final decrypted plaintext to `/home/user/recovered_evidence.txt`.
   - Ensure that the file `/home/user/recovered_evidence.txt` has exactly `0400` file permissions (read-only for the owner, no permissions for anyone else) to maintain the chain of custody.

Compile your C code, execute the full extraction pipeline, and verify the final evidence file exists with the correct contents and permissions.