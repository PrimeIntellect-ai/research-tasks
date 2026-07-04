You are a security engineer tasked with securing an internal legacy C++ authentication service. You are currently in the middle of rotating cryptographic credentials, but you discovered that the existing service has a critical vulnerability. It implements a custom token validation logic similar to JSON Web Tokens (JWT) but is vulnerable to an `alg=none` bypass, allowing unauthenticated attackers to forge administrator tokens. Additionally, the service runs without any process isolation.

Your task consists of three phases: Exploit, Patch, and Sandbox.

**Phase 1: Exploit Crafting**
The source code for the authentication service is located at `/home/user/auth_service/auth_server.cpp`. It expects tokens in the format `HEADER.PAYLOAD.SIGNATURE` (base64 encoded JSON). 
1. Analyze the C++ code to understand the `alg=none` vulnerability.
2. Craft a malicious token that claims the identity `{"role":"admin"}` but bypasses signature verification.
3. Save this exact raw base64-encoded token string into a file at `/home/user/auth_service/exploit.jwt`.

**Phase 2: Secure Coding & Certificate Validation**
1. Modify `/home/user/auth_service/auth_server.cpp` to fix the vulnerability.
2. Ensure that if the algorithm specified in the header is "none", "NONE", or empty, the `validate_token` function immediately returns `false`.
3. The current implementation also has a commented-out section for certificate chain depth validation. Implement a simple check in the `verify_cert_chain` function: it should return `false` if the `chain_depth` parameter is less than 2.
4. Compile the service using the provided `Makefile` in the `/home/user/auth_service` directory. The output executable will be `auth_server`.

**Phase 3: Process Isolation**
To defense-in-depth, the service must be run in a sandbox. 
1. Create a script at `/home/user/auth_service/start_sandboxed.sh`.
2. The script must use `bwrap` (Bubblewrap) to execute `./auth_server`.
3. The sandbox must enforce the following constraints:
   - Bind mount the root filesystem `/` as read-only.
   - Bind mount `/dev` and `/proc` appropriately (`--dev /dev`, `--proc /proc`).
   - Provide a read-write tmpfs mounted at `/tmp`.
   - Unshare all namespaces (e.g., `--unshare-all`).
   - Drop all privileges (run as the current user UID/GID).
4. Ensure the script is executable.

Output exactly what is requested. Automated tests will verify the existence and contents of `exploit.jwt`, compile your patched `auth_server.cpp` to ensure it rejects the exploit, and inspect `start_sandboxed.sh` for the correct `bwrap` configuration.