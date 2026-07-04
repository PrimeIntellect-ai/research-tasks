You are a penetration tester tasked with building a custom automated vulnerability scanning utility in C and performing SSH hardening on a target configuration file.

Your objectives:
1. Write a C program at `/home/user/scanner.c`.
2. The program should accept exactly three command-line arguments:
   - `argv[1]`: Path to an SSH configuration file to scan.
   - `argv[2]`: Path to output the encrypted vulnerability report.
   - `argv[3]`: A 256-bit AES key represented as a 64-character hex string.

3. **Vulnerability Scanning**:
   - The program must open and read the SSH config file specified in `argv[1]`.
   - It should search for lines containing exactly `PermitRootLogin yes` or `PasswordAuthentication yes` (you can assume exact matches, no leading/trailing spaces for these tokens, ignoring lines that are commented out with `#`).
   - Construct a JSON report of the findings. The JSON must be strictly formatted without extra spaces:
     `{"vulnerabilities":["PermitRootLogin","PasswordAuthentication"]}`
     If only one is found, format it as `{"vulnerabilities":["PermitRootLogin"]}` (or `PasswordAuthentication`). If both are found, `PermitRootLogin` must appear first. If none are found, output `{"vulnerabilities":[]}`.

4. **Encryption**:
   - Encrypt the JSON string (do not include the null terminator in the plaintext) using AES-256-CBC.
   - Use the key provided in `argv[3]` (convert it from hex to binary bytes).
   - Use an Initialization Vector (IV) consisting of exactly 16 bytes of zeros (`0x00`).
   - Use standard PKCS#7 padding (which is the default in OpenSSL's EVP API).
   - Write the raw binary ciphertext to the output file specified in `argv[2]`.

5. **Compilation & Execution**:
   - Compile the program to `/home/user/scanner` using `gcc`. You are permitted to link against OpenSSL (`-lcrypto`).
   - An SSH config file is located at `/home/user/target_sshd_config` and a key is at `/home/user/aes_key.txt`.
   - Run your program to scan the config and generate the encrypted report at `/home/user/report.enc`:
     `./scanner /home/user/target_sshd_config /home/user/report.enc $(cat /home/user/aes_key.txt)`

6. **SSH Hardening**:
   - After generating the report, manually harden the `/home/user/target_sshd_config` file.
   - Change `PermitRootLogin yes` to `PermitRootLogin no`.
   - Change `PasswordAuthentication yes` to `PasswordAuthentication no`.
   - Do not remove or modify other configuration lines.

Ensure all file paths and formatting strictly match the instructions.