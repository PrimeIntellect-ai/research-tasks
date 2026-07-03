You are a security engineer responsible for securely rotating credentials for an internal service. 

An incomplete C++ credential rotation tool is located at `/home/user/app/rotate_creds.cpp`. Your task is to secure and complete this program, then run it to generate the new credentials.

The existing code is vulnerable and lacks proper isolation and integrity checks. You must fix it by implementing the following requirements in `/home/user/app/rotate_creds.cpp`:

1. **File Integrity Verification:** The program must read the configuration file `/home/user/app/config.json`. Before processing, it must compute the SHA256 hash of the file's contents and verify it matches the expected hash stored in `/home/user/app/config.json.sha256`. If the hash does not match, the program must terminate immediately.
2. **Authentication Flow Fix (Privilege Escalation Prevention):** The code contains a hardcoded bypass flag (`admin_override = true`) that skips the secure key derivation. You must remove this bypass. The new credential must be securely derived simply by taking the value of the `master_key` from the JSON and appending the string `_ROTATED`.
3. **Process Isolation (Sandboxing):** The generation of the new credential and the writing of the output must occur in a sandboxed state. You must use Linux's strict seccomp mode (`prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT, ...)`). 
    * *Hint:* Strict seccomp only allows `read`, `write`, `_exit`, and `sigreturn`. You must open all necessary files (like `/home/user/app/new_creds.txt`) and do any operations that require other syscalls (like memory allocation for SHA256) *before* activating the sandbox.
    * *Hint:* Use `_exit(0)` instead of `return 0;` or `exit(0);` at the end of your program, as standard exit functions may invoke unsupported syscalls.

**Setup Instructions for you:**
Before you begin modifying the C++ code, you should create the initial files if they don't exist:
1. Create `/home/user/app/config.json` with the exact content: `{"master_key":"secR3t_k3Y_991"}`
2. Create `/home/user/app/config.json.sha256` containing the valid SHA256 checksum of the `config.json` file.

**Execution:**
Once the C++ file is complete, compile it using `g++ -O2 -o /home/user/app/rotate_creds /home/user/app/rotate_creds.cpp -lcrypto`.
Run the binary.

**Success Criteria:**
- The binary successfully writes the derived credential to `/home/user/app/new_creds.txt`.
- The source code must contain `SECCOMP_MODE_STRICT` and properly isolate the credential derivation and writing phase.
- The binary must not crash from a seccomp violation (SIGKILL).