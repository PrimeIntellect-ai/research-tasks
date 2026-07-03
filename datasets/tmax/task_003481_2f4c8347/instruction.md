You are a security auditor tasked with checking access tokens used for temporary SSH access. We use a C++ utility to validate these JSON Web Tokens (JWTs). 

Currently, the utility project is located in `/app/auditor-tool/`. It vendors the `jwt-cpp` library in `/app/auditor-tool/vendor/jwt-cpp/`. However, the build system has been slightly damaged by a junior developer, and the token validation logic in `main.cpp` is incomplete.

Your tasks are:
1. **Fix the Build**: The `/app/auditor-tool/CMakeLists.txt` is missing the correct OpenSSL linking instructions, causing linker errors during compilation. Fix the `CMakeLists.txt` so the project can be built successfully using `cmake -B build && cmake --build build`.
2. **Implement Validation**: Complete the C++ code in `/app/auditor-tool/main.cpp`. The program will receive the path to a token file as its first command-line argument. It must read the token and print exactly `VALID` to standard output if the token is secure and valid, or `INVALID` if it fails any security checks.
3. **Security Rules**: A token is considered `VALID` strictly if:
   - It is signed with the `HS256` algorithm using the secret key: `ssh-audit-secret-2024`.
   - It is NOT expired (check the `exp` claim).
   - The payload contains a `role` claim with the exact string value `auditor`.
   - It does NOT use the `"none"` algorithm (which circumvents signature checks).

You can test your implementation against two datasets provided:
- `/app/corpus/clean/`: Contains strictly valid tokens. Your program MUST output `VALID` for all files in this directory.
- `/app/corpus/evil/`: Contains forged, expired, or malicious tokens. Your program MUST output `INVALID` for all files in this directory.

Ensure your compiled executable is located at `/app/auditor-tool/build/validator` and works as described.