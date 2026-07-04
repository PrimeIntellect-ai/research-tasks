You are a security engineer tasked with rotating credentials and securing a legacy authentication service. 

The service is located in `/home/user/auth_service`. Inside this directory, you will find:
1. `auth.c`: The source code for the authentication service, which uses an SQLite backend. It contains a critical SQL injection vulnerability.
2. `users.db`: An SQLite database containing user credentials.
3. `hasher`: A compiled Linux ELF binary (without source code) that implements a custom hashing algorithm used by the application. It takes a plaintext string as an argument and outputs a hex-encoded hash.

Your tasks are as follows:

1. **Vulnerability Analysis & Secure Coding**: Analyze `auth.c` and identify the SQL injection vulnerability in the authentication logic. Modify `auth.c` to fix the vulnerability by replacing the insecure string concatenation with parameterized queries (`sqlite3_prepare_v2`, `sqlite3_bind_text`, etc.).
2. **Compile**: Compile your fixed code into a new executable named `/home/user/auth_service/auth_fixed`. Make sure to link the `sqlite3` library (`-lsqlite3`).
3. **Reverse Engineering**: Disassemble and analyze the `hasher` binary to understand its custom hashing algorithm. It performs a simple single-byte XOR operation on each character before hex-encoding the output. Identify the single-byte XOR key. Write the XOR key in hex format (e.g., `0xAB`) to `/home/user/xor_key.txt`.
4. **Decryption**: Extract the current hashed password for the `admin` user from `users.db`. Using the XOR key you discovered, reverse the hash to find the plaintext password. Save this plaintext password to `/home/user/old_password.txt`.
5. **Credential Rotation**: Generate the hash for the new password `Secure_Rotated_2024` using the custom hashing algorithm. Update the `users.db` database so that the `admin` user has this new password hash.

Ensure all output files (`xor_key.txt`, `old_password.txt`) contain only the requested values with no extra text.