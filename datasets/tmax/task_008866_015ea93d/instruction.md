You are a security engineer responsible for rotating credentials and securing a legacy data processing pipeline. 

Your team is migrating from an old C++ binary (`/home/user/legacy_auth_worker`) to a new source version (`/home/user/new_auth_worker.cpp`). During this credential rotation, you need to extract the old hardcoded password for auditing, and fix a critical injection vulnerability in the new code before compiling it.

Perform the following steps:

1. **Binary Analysis & Credential Extraction**: 
   The compiled ELF executable `/home/user/legacy_auth_worker` contains a hardcoded legacy password used for remote SSH authentication. The password string in the binary is prefixed with `AUTH_PWD:` (e.g., `AUTH_PWD:example_password`). 
   Extract the actual password (without the prefix) and save it exactly as a single line in `/home/user/old_password.txt`.

2. **Vulnerability Analysis & Secure Coding**:
   Analyze the C++ source code in `/home/user/new_auth_worker.cpp`. It contains a command injection vulnerability in the `check_host` function where user input is directly concatenated into a `system()` call to execute a ping command.
   Fix the vulnerability by completely removing the `system(...)` call. Replace it with the securely implemented `safe_ping(host)` function which is already defined in the file. Ensure the logic remains the same (return `true` if `safe_ping` succeeds, `false` otherwise).

3. **Compilation**:
   Compile the patched `/home/user/new_auth_worker.cpp` into a new executable located at `/home/user/new_auth_worker_fixed`. Use `g++` with standard compilation flags (e.g., `g++ -std=c++17 /home/user/new_auth_worker.cpp -o /home/user/new_auth_worker_fixed`).

Constraints:
- Do not change the signature of `check_host`.
- Do not leave any `system()` calls in the file.
- The output in `/home/user/old_password.txt` must contain only the extracted password, no extra spaces or newlines other than the trailing newline.