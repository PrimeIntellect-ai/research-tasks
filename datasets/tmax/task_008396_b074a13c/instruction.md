You are an incident responder investigating a suspicious proprietary authentication service on a compromised Linux server. The service generates and validates access tokens for remote workers, but attackers have been bypassing it to gain unauthorized access.

The source code and build files for the service are located in `/home/user/incident/`.

Your investigation requires you to complete the following tasks:

1. **Code Auditing & Vulnerability Identification**: 
   Audit `/home/user/incident/auth_server.cpp`. Identify the two critical security vulnerabilities present in the code:
   - A cryptographic flaw in how the access tokens are generated.
   - A memory corruption vulnerability in the token parsing logic.

2. **C++ Patching & Remediation**:
   Modify `auth_server.cpp` to fix both vulnerabilities. 
   - Replace the weak token generation with a cryptographically secure method using standard modern C++ features (`std::random_device`, etc.) or `/dev/urandom`.
   - Fix the memory corruption vulnerability by using safe string handling.

3. **Process Isolation / Sandboxing**:
   The service currently runs with too many privileges. Modify the C++ code to implement a `seccomp` filter (using `libseccomp`) immediately after the server initializes, right before it begins processing tokens. The sandbox must restrict the process to ONLY allow the following syscalls: `read`, `write`, `close`, `exit`, `exit_group`, and `rt_sigreturn`. 

4. **Building**:
   Update the `Makefile` in `/home/user/incident/` to link against the necessary seccomp libraries, and build the updated binary by running `make`. The resulting binary must be located at `/home/user/incident/authd`.

5. **Reporting**:
   Generate an incident report at `/home/user/incident_report.json` with exactly the following structure:
   ```json
   {
     "vulnerabilities": [
       "CWE-XXX",
       "CWE-YYY"
     ],
     "sandboxing_library_used": "..."
   }
   ```
   Replace `XXX` and `YYY` with the correct official CWE IDs for the Weak PRNG and the Classic Buffer Overflow vulnerabilities you identified. Replace the `sandboxing_library_used` value with the name of the shared object library you linked against.

Constraints:
- Do not use root/sudo. The environment will have standard tools available.
- You may need to install missing development packages in your user space or use standard system packages if already available (assume `libseccomp-dev` can be installed or is present).