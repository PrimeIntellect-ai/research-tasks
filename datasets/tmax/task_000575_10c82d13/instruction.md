You are a security engineer analyzing a suspicious network service deployed on your system. You need to secure the application, isolate it, and audit the environment.

Perform the following tasks:

1. **TLS Certificate Management**: 
   The service requires TLS certificates to run, but they are missing. Create a directory `/home/user/pki`. Generate a 2048-bit RSA private key (`server.key`) and a self-signed X.509 certificate (`server.crt`) valid for 365 days with the Common Name (CN) set to `localhost`. Place both files in `/home/user/pki/`.

2. **Vulnerability Analysis & Secure Coding (C++)**: 
   You have been provided the source code of the service at `/home/user/server.cpp`. The function `bool validate_token(const std::string& token)` contains a critical authentication bypass vulnerability (similar to the JWT `alg=none` flaw) where it accepts tokens ending in `|sig:none`. 
   Patch the C++ code so that it strictly rejects `|sig:none` and ONLY accepts tokens where the signature matches exactly `|sig:VALID_MAC`. Compile the patched code to `/home/user/server` using `g++ /home/user/server.cpp -o /home/user/server`.

3. **Process Isolation and Sandboxing**: 
   To prevent future exploits from compromising the host, write a shell script at `/home/user/run_secure.sh` that uses `bwrap` (Bubblewrap) to run the compiled `/home/user/server`. The sandbox must:
   - Isolate the network (`--unshare-net`)
   - Mount the root filesystem as read-only (`--ro-bind / /`)
   - Bind mount the PKI directory read-only (`--ro-bind /home/user/pki /home/user/pki`)

4. **Privilege Escalation Auditing**: 
   There is a directory `/home/user/test_env` that contains various binaries. To ensure no local privilege escalation vectors exist in this directory, find all files with the SUID bit set within `/home/user/test_env`. Write the absolute paths of these files, one per line, to `/home/user/suid_audit.txt`.

Ensure all files are created exactly at the specified paths.