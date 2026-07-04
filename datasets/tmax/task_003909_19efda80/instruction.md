You are an incident responder investigating a compromised Linux host. You have discovered a suspicious directory at `/home/user/incident/` containing artifacts from a malicious beacon.

The directory contains:
- `beacon.elf`: A compiled Linux executable.
- `payload.enc`: An encrypted configuration payload.
- `certs/`: A directory containing three certificates: `ca.crt`, `intermediate.crt`, and `leaf.crt`.

Your investigation requires you to perform the following steps:

1. **Reverse Engineering**: Analyze `beacon.elf` to extract the 16-byte symmetric encryption key. The malware author hardcoded this key in the binary (likely near a crypto initialization function).
2. **Secure Coding & Certificate Validation**: Write a C program at `/home/user/decryptor.c`. This program must use the OpenSSL library to programmatically validate the certificate chain (`leaf.crt` -> `intermediate.crt` -> `ca.crt`). The program must print "CERT_CHAIN_VALID" to standard output if the chain is fully valid.
3. **Decryption**: If the certificate chain is valid, your C program must decrypt the contents of `payload.enc` using the key you extracted from the binary. 
    - The algorithm used is AES-128-CBC.
    - The Initialization Vector (IV) is known to be the hex sequence: `0102030405060708090a0b0c0d0e0f10`.
    - The payload contains padding.
4. **Extraction**: The decrypted payload contains a string in the format `C2_SERVER=<IP_ADDRESS>`. Extract this IP address and save it to a new file exactly at `/home/user/c2_indicator.txt`.

Constraints & Requirements:
- You must write the solution in C (`/home/user/decryptor.c`) and compile it. You can use OpenSSL (`-lcrypto -lssl`).
- Do not use command-line tools like `openssl enc` or `openssl verify` to perform the final validation/decryption; you must write the C code to do this. You may use command-line tools (like `strings`, `objdump`, `gdb`, `xxd`) for the reverse engineering phase.
- Ensure the extracted IP address in `/home/user/c2_indicator.txt` has no trailing spaces or newlines other than a single standard newline.