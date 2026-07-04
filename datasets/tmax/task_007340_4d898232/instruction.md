You are a security-conscious network engineer taking over a poorly configured traffic inspection environment. You need to secure the environment, fix a vulnerability in the authentication parser, and prepare test assets.

Perform the following tasks:

1. Privilege Escalation Auditing:
There is a compiled binary at `/home/user/bin/legacy_monitor`. It was deployed with dangerous permissions that could allow privilege escalation. Audit and fix its permissions so that it is readable, writable, and executable by the owner, and readable and executable by the group and others, but WITHOUT any setuid or setgid bits.

2. Binary Format and ELF Analysis & TLS/SSL Certificate Management:
The `/home/user/bin/legacy_monitor` binary hardcodes a specific file path where it expects to find a trusted Root CA certificate. Analyze the ELF binary to find this hardcoded path (it is a `.crt` file inside a hidden directory in `/home/user/`). 
Once you find the path, generate a new self-signed X.509 certificate (valid for 365 days, RSA 2048-bit) and save it exactly at that hardcoded path. Ensure the parent directories exist.

3. Secure C++ Coding (JWT "alg: none" bypass):
You have the source code for the new token validator at `/home/user/jwt_auth.cpp`. Currently, it contains a vulnerability: it blindly accepts JSON Web Tokens (JWTs) even if the header specifies `"alg": "none"`. 
Modify `/home/user/jwt_auth.cpp` so that the `validate_algorithm(const std::string& header_json)` function returns `false` if the algorithm is "none" (case-insensitive) or if the "alg" field is missing.
Compile the fixed source code using `g++ /home/user/jwt_auth.cpp -o /home/user/jwt_auth`.

4. Exploit Generation:
To test the fix, manually craft a forged JWT that exploits the "alg: none" vulnerability. 
The token must:
- Have a standard base64url-encoded JWT header specifying `"alg": "none"` and `"typ": "JWT"`.
- Have a base64url-encoded payload of exactly `{"role":"admin"}`.
- Have NO signature (the third part of the JWT should be empty, but the two periods must still be present, e.g., `header.payload.`).
Save this exact token string to a file at `/home/user/bad_token.txt`.