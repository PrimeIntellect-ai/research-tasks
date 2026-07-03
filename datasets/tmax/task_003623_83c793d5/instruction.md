You are a security engineer tasked with rotating credentials for a legacy authentication service on a Linux system. 

You have been given a compiled, undocumented binary located at `/home/user/legacy_auth`. This service authenticates users by reading a password from standard input, appending a hardcoded salt to it, hashing the combined string using SHA256, and comparing the result against a hex-encoded hash stored in `/home/user/auth_config.txt`. 

Your goal is to reverse engineer the binary to find the salt, rotate the password to `Nova_Core_77X!`, and write an automated C++ utility that performs the rotation and tests the authentication flow under strict process isolation.

Here are your specific requirements:

1. **Reverse Engineering**: Analyze `/home/user/legacy_auth` to extract the hardcoded salt string.
2. **C++ Credential Rotator**: Write a C++ program named `/home/user/rotate_cred.cpp` (and compile it to `/home/user/rotate_cred`) that does the following:
   - Computes the SHA256 hash of the new password (`Nova_Core_77X!`) combined with the extracted salt. The OpenSSL library (`-lcrypto`) is installed and available for you to use.
   - Overwrites `/home/user/auth_config.txt` with the newly computed hex-encoded SHA256 hash.
   - **Process Isolation**: Spawns `/home/user/legacy_auth` as a child process using `fork()` and `execve()`. To satisfy sandboxing requirements, you **must** ensure the child process is executed with a completely empty environment (the `envp` array passed to `execve` must have `NULL` as its first and only element). The legacy binary contains anti-tamper checks and will immediately reject authentication if it detects any environment variables.
   - **Auth Flow Testing**: Feed the new password (`Nova_Core_77X!`) to the isolated child process's standard input via an inter-process pipe.
   - Read the standard output from the child process.
3. **Logging**: Your C++ program must write the results to `/home/user/rotation_log.txt` in exactly the following format:
   ```
   SALT=<the_extracted_salt>
   HASH=<the_new_hex_encoded_sha256_hash>
   RESULT=<the_exact_stdout_from_the_legacy_binary>
   ```

Ensure your C++ code is robust, correctly handles the pipes/forks, and properly null-terminates the environment array for `execve`. Once finished, run your compiled `rotate_cred` tool to generate the `rotation_log.txt` file.