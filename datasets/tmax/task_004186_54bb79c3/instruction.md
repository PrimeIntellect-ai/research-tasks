You are a security auditor reviewing a vulnerable authentication service. 
You discovered that the current C++ service passes sensitive passwords via command-line arguments, which makes them visible to any user on the system via `/proc/[pid]/cmdline`.

Your task is to fix this vulnerability by modifying the application to securely read from a vault file, process the credential securely, and enforce strict access controls.

Here is what you must do:

1. **Fix File Permissions**: The password is now stored in `/home/user/vault.txt`. Secure this file by changing its permissions so that ONLY the owner has read access (exactly `0400`). Remove all other permissions.

2. **Secure the Code**: Modify the source code located at `/home/user/auth_service.cpp`. 
   Instead of taking the password from `argv[1]`, the program must:
   - Read the password directly from `/home/user/vault.txt`.
   - Strip any trailing newlines from the read password.
   - Compute the SHA-256 hash of the password.
   - Base64 encode the raw binary SHA-256 digest.
   - Write ONLY the resulting Base64 string to `/home/user/secure_hash.log` and exit.

3. **Compile and Run**:
   Compile your updated code to an executable named `/home/user/auth_service_secure`. You may use the OpenSSL library for hashing and encoding (`-lcrypto`).
   Execute your compiled program so that `/home/user/secure_hash.log` is generated.

Ensure you leave the system in exactly this state, as an automated test will verify the file permissions, the existence of the compiled binary, and the exact contents of the log file.