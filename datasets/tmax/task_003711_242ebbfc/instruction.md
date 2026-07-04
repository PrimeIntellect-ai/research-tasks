You are a compliance analyst tasked with generating an audit trail of malicious authentication attempts. 

You have been provided with two files in your home directory (`/home/user`):
1. `/home/user/server.log`: A log file containing recent token-based authentication attempts. Each line follows the format: `[TIMESTAMP] IP: <ip_address> - Token: <token_string>`
2. `/home/user/validate.c`: A C source file for a standalone utility that validates the cryptographic integrity of a given token.

Your task is to:
1. Compile `/home/user/validate.c` into an executable named `validate` in the same directory.
2. The `validate` program takes exactly one argument (the token string). It exits with status code `0` if the token is cryptographically valid, and `1` if the token is invalid (forged or corrupted).
3. Parse `/home/user/server.log` and use the compiled `validate` utility to check every token.
4. Correlate the failed token validations with their source IP addresses.
5. Generate an audit report file at `/home/user/blocked_ips.txt` containing only the unique IP addresses that submitted at least one **invalid** token. The IP addresses in the file must be sorted in standard ascending numerical order (e.g., using `sort -V`), with exactly one IP address per line.

Do not include any valid IP addresses or other text in the output file. You must rely purely on standard Linux shell built-ins, coreutils, and the provided C code.