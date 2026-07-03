You are a security auditor tasked with reviewing a custom authorization mechanism on a legacy Linux server. During your audit of the permissions, you discovered an undocumented, stripped executable located at `/app/auth_validator`. 

The system administrators claim this binary is used to encrypt and validate authorization tokens, but the source code has been lost. You suspect the encryption algorithm is weak (a homebrew cipher) and may contain security vulnerabilities, but to prove this and to migrate away from the black-box binary, you need to understand exactly how it works.

Your objective is to reverse-engineer the `/app/auth_validator` binary and write a pure Bash script that behaves identically. 

Instructions:
1. Analyze the stripped binary `/app/auth_validator` to determine its cryptographic transformation algorithm. You may use standard reverse-engineering tools available in a Linux environment (e.g., `strings`, `strace`, `ltrace`, `gdb`, `objdump`).
2. Implement the exact same transformation logic in a Bash script located at `/home/user/check_perm.sh`.
3. Your script must be written entirely in Bash (using standard coreutils like `awk`, `sed`, `tr`, `printf`, etc., is allowed).
4. Your script must take exactly one argument (an ASCII token string) and print the transformed output to `stdout`, exactly matching the output format of the original binary.

Example behavior of the target binary:
`/app/auth_validator "secret_token"` -> `[some hex or encoded output]`

Your script `/home/user/check_perm.sh` must produce the exact same bit-for-bit output as `/app/auth_validator` for any given input string containing standard printable ASCII characters. Ensure the script is executable (`chmod +x /home/user/check_perm.sh`).