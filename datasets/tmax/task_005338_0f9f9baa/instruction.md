You are a DevSecOps engineer enforcing security policies. We have a legacy system that manages SSH access via a web interface, but it has several security issues. You need to analyze the system, crack a poorly encrypted authentication token, fix a privilege escalation vulnerability in a C program, and enforce SSH hardening policies.

Perform the following tasks:

1. **HTTP Cookie Inspection & Cryptanalysis**:
   - Read the raw HTTP request in `/home/user/http_request.txt`.
   - Extract the hex-encoded value of the `session_token` cookie.
   - The token was encrypted using a custom weak cipher. We know the original plaintext token starts with the string `"AUTH_TOKEN_"`.
   - The encryption algorithm (which you can deduce) XORs each byte of the plaintext with a single 8-bit secret key, and then adds the byte's index (0-based) to the result modulo 256. 
   - Write a script or C program to perform a known-plaintext attack to recover the 1-byte secret key and decrypt the entire token.
   - Save the fully decrypted plaintext token to `/home/user/decrypted_token.txt`.

2. **Privilege Escalation Auditing & Secure Coding in C**:
   - The system uses a C program located at `/home/user/key_manager.c` to append SSH keys to the authorized_keys file.
   - Currently, the C program uses the insecure `system()` function to echo the input into the file, which is vulnerable to shell command injection (a critical privilege escalation risk if this binary were setuid).
   - Rewrite `/home/user/key_manager.c` so that it uses secure C file I/O functions (`fopen`, `fprintf`, `fclose`) to append the provided SSH key string (the first command-line argument) to the file `/home/user/managed_authorized_keys` safely, completely removing the `system()` call.
   - Ensure the program returns `0` on success and `1` on failure (e.g., if the file cannot be opened).
   - Compile your fixed C program to `/home/user/key_manager`.

3. **SSH Hardening**:
   - We need to enforce policy as code on our SSH configuration.
   - Edit the file `/home/user/sshd_config`.
   - Ensure that `PermitRootLogin` is explicitly set to `no`.
   - Ensure that `PasswordAuthentication` is explicitly set to `no`.
   - Remove or comment out any conflicting directives for these two settings.

Ensure all outputs are exactly at the specified paths.