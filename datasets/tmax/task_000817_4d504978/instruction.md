You are a penetration tester tasked with auditing a set of local microservices. Your goal is to build an automated auditing tool in C++ that checks for configuration anomalies, file permission flaws, and broken authentication tokens. 

You have been provided with a vendored C++ authentication auditing library located at `/app/sec-audit-lib-1.0`. However, the previous developer left it in a broken state. 

**Stage 1: Fix the Vendored Library**
1. Inspect the source code and build system in `/app/sec-audit-lib-1.0`. 
2. The `Makefile` is missing a critical linker flag required for cryptographic operations.
3. The file `src/token_validator.cpp` contains a critical logic flaw where signature verification is bypassed (hardcoded to always return true). 
4. Fix the code and Makefile, then compile the library to produce `libsecaudit.a`.

**Stage 2: Develop the Auditing Tool**
Write a C++ program (e.g., `audit_tool.cpp`) that utilizes your fixed library. The program must perform the following workflow:
1. Read the target list from `/home/user/targets.txt`. Each line is formatted as: `Port,ConfigFilePath,ExpectedSHA256`
2. **Integrity & Permissions Check:** For each target, compute the SHA256 hash of the `ConfigFilePath`. 
   - If the hash does not match `ExpectedSHA256`, record the status as `TAMPERED`.
   - If the hash matches, check the file permissions. If the file is world-writable (e.g., `o+w`), record the status as `VULNERABLE_PERMS`.
3. **Service Auditing (Port Scan & Token):** If the file is intact and permissions are secure, connect to the local TCP `Port`. 
   - The service will immediately send a session token (a string ending in a newline).
   - Use the fixed `sec-audit-lib-1.0` (specifically the `SecAudit::ValidateToken(const std::string& token)` function) to validate the received token.
   - If the token is invalid, record `VULNERABLE_TOKEN`.
   - If the token is valid, record `SECURE`.

**Stage 3: Output**
Your C++ program must write the final audit results to `/home/user/audit_results.csv`.
The format must strictly be:
```csv
Port,Status
8001,SECURE
8002,VULNERABLE_PERMS
...
```

**Evaluation**
Your output will be evaluated against a hidden reference dataset. Your solution must achieve an Accuracy metric of >= 0.95 across all simulated services.