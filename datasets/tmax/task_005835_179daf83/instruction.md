You are a DevSecOps engineer enforcing policy-as-code and incident response protocols. We have discovered a vulnerability in an unmaintained, legacy authentication binary located at `/home/user/legacy_auth`. We no longer have the source code for this binary. 

The binary is used to validate administrative tokens and has been mistakenly leaking its hardcoded secret salt into log files. 

Your task consists of the following steps:

1. **Reverse Engineering:** Analyze the compiled binary `/home/user/legacy_auth` to discover the hardcoded secret salt. The salt is a 12-character alphanumeric string. 

2. **Token Generation (C Language):** Through previous analysis, we know the binary validates tokens by checking if the provided token matches the lowercase hexadecimal representation of the username XORed byte-by-byte with the hardcoded salt. (If the username is longer than the salt, the salt wraps around and repeats). 
   Write a C program at `/home/user/keygen.c` that accepts a username as its first command-line argument and prints the valid hexadecimal token. Compile this program to `/home/user/keygen`.

3. **Exploit/Auth Bypass:** Use your compiled `keygen` to generate a valid token for the username `sysadmin_prod`. Run the legacy binary with this credential format: 
   `/home/user/legacy_auth sysadmin_prod:<generated_hex_token>`
   If successful, the binary will print an access granted message and a flag. Save the exact standard output of this successful execution to `/home/user/success.txt`.

4. **Sensitive Data Redaction:** The log file `/home/user/logs/auth.log` contains historical debug traces that leak the plaintext secret salt. Write a shell command or script to redact the exact 12-character salt string from this file, replacing every instance of it with the exact string `[REDACTED]`. Save the cleaned log to `/home/user/logs/auth_clean.log`.

Constraints:
- All files must be created in the exact paths specified.
- Do not modify the original `/home/user/logs/auth.log` file.
- The C program must compile without errors using standard `gcc`.