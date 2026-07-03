You are an incident responder investigating a compromised server. The attacker managed to insert a malicious SSH key and exploit a weakness in a custom C++ authorization daemon to forge an admin token.

Your objectives:
1. **SSH Hardening**: The file `/home/user/.ssh/authorized_keys` contains multiple SSH keys. Identify and remove the key associated with the attacker's email `evil@hacker.com`. Leave the other keys intact.

2. **Cryptanalysis & Token Forgery**:
   You have discovered the source code for the authorization daemon at `/home/user/auth_daemon.cpp`. The daemon uses a weak custom token generation algorithm that relies on the system time (`timestamp`) to seed a random number generator (`srand(timestamp)`), which is then used to XOR the username.
   The attacker generated an admin token using the specific timestamp `1700000000`.
   Write a C++ program (e.g., `/home/user/exploit.cpp`) that replicates this flawed logic to generate the exact token the attacker forged for the username `admin` at timestamp `1700000000`.
   Save the forged `admin` token string directly into `/home/user/admin_token.txt`.

3. **Secure Coding**:
   The current token generation is insecure. Modify `/home/user/auth_daemon.cpp` to use a secure cryptographic hash function instead of the weak PRNG XOR method. 
   Specifically, rewrite the `generate_token` function to return the SHA-256 hash (in lowercase hex format) of the `username` concatenated with the string `"SecureSecretKey"`. You should use OpenSSL's `SHA256` function (ensure to include `<openssl/sha.h>`).
   Compile your fixed code to `/home/user/auth_daemon_fixed` (link against the `crypto` library).

Deliverables:
- Cleaned `/home/user/.ssh/authorized_keys`
- Forged token saved in `/home/user/admin_token.txt`
- Fixed and compiled binary `/home/user/auth_daemon_fixed`