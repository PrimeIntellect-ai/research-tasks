As a compliance analyst, you are auditing a legacy web server that previously suffered from an open redirect vulnerability in its login flow. To fix it, the developers implemented a custom token-based signature for redirect URLs, tied to the server's active TLS certificate thumbprint and a secret 4-digit PIN assigned to each privileged user. 

You need to generate an audit trail to ensure none of the privileged users are using easily guessable PINs (e.g., standard sequences or repeated digits), which could lead to privilege escalation if an attacker bypasses the redirect protection.

You are provided with:
1. A stripped, compiled binary at `/app/token_gen` which the server uses to generate the tokens. It takes two arguments: the TLS certificate thumbprint and the 4-digit PIN. 
   Example usage: `/app/token_gen A1B2C3D4E5 1234`
2. An audit log file at `/home/user/redirect_logs.txt` containing 500 observed redirect tokens. Each line is formatted as: `<tls_cert_thumbprint>,<redirect_token>`.

Your objective is to recover the 4-digit PIN for each line in the log. Because there are 500 entries and 10,000 possible PINs for each, using a shell script to call the binary 5,000,000 times will be far too slow. You must analyze the `/app/token_gen` binary to determine the underlying hashing algorithm it uses, then write a highly optimized brute-force cracking tool in **C**. 

Compile your C program, run it against the logs, and output the recovered PINs to a new file at `/home/user/recovered_pins.txt`. 
The output format must be strictly: `<tls_cert_thumbprint>,<4-digit-pin>` (one per line, matching the order of the input file).

Do not modify the original log file. You have the standard C toolchain (gcc), OpenSSL (`libssl-dev`), and reverse engineering tools (`strings`, `objdump`, `xxd`) available.