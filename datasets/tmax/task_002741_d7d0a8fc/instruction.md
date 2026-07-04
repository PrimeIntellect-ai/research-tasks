You are a forensics analyst recovering evidence from a compromised host. We suspect an attacker exploited a custom C++ authentication service using a forged JWT (JSON Web Token) vulnerability, specifically a variant of the "algorithm=none" exploit.

We have extracted the source code for the custom JWT library the service used. It is vendored at `/app/custom-jwt-cpp-1.0`. However, the attacker attempted to sabotage our investigation by corrupting the package's build scripts. 

Your tasks are as follows:

1. **Repair the Vendored Package:**
   Inspect `/app/custom-jwt-cpp-1.0`. The build system (CMake) is broken due to a deliberate perturbation (a missing include path and an incorrectly named environment variable required for compilation). Fix the package so it can be built and linked against.

2. **Implement the Forensic Token Analyzer:**
   Using the repaired library, write a C++ program at `/home/user/token_analyzer.cpp` and compile it to `/home/user/token_analyzer`. 
   
   The program must accept a single command-line argument: a raw JWT string.
   
   The program must parse the token and simulate the compromised authentication logic:
   - If the token's header specifies `"alg": "none"` (case-insensitive) and the payload contains the claim `"role": "admin"`, the program must output the SHA-256 hash of the entire base64-decoded payload, followed by a newline, and exit with code 0.
   - If the token has any other algorithm or is missing the admin role, output `INVALID` followed by a newline, and exit with code 1.
   - If the token is malformed, output `MALFORMED` followed by a newline, and exit with code 2.

Your implementation must be bit-exact equivalent in its output and exit codes to a reference binary we recovered. Our automated verification system will heavily fuzz your `/home/user/token_analyzer` binary against our reference oracle using thousands of generated tokens.