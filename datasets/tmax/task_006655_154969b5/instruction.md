You are acting as a security auditor. We suspect that a background process running on this system is leaking a sensitive authentication token by passing it as a command-line argument, making it visible to anyone who can read the process list or `/proc`.

Your task consists of three parts:

1. **Vulnerability Analysis & Token Discovery**: 
   Identify the looping background process running on the system that is executing `/home/user/auth_tool`. Extract the leaked plaintext token from its command-line arguments.

2. **Cryptographic Verification**:
   Compute the SHA256 hash of the extracted token (just the token string, no trailing newlines). Save this SHA256 hash to a file located precisely at `/home/user/token_hash.txt`.

3. **Secure Remediation**:
   The `auth_tool` actually supports receiving the token via an environment variable named `SECRET_TOKEN`, which prevents the `/proc` visibility leak. 
   Write a secure wrapper script located at `/home/user/secure_invoke.sh` that does the following:
   - Reads the token from a file named `/home/user/token.txt` (assume this file will be created by the system administrator with strict permissions; you do not need to create it, but write your script to read from it).
   - securely invokes `/home/user/auth_tool` by passing the token exclusively via the `SECRET_TOKEN` environment variable.
   - Does NOT pass the token as a command-line argument.
   - Make sure your script `/home/user/secure_invoke.sh` is executable.

Ensure your wrapper script properly isolates the secret within the environment of the executed process and avoids any command-line parameter leakage.