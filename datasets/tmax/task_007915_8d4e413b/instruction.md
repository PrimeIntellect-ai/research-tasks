You are a security engineer tasked with rotating credentials and patching a vulnerability in a custom C++ CGI authentication handler.

We have a legacy CGI binary that handles login redirects. It has been reported that this binary contains an Open Redirect vulnerability, and its cryptographic secret key needs to be rotated.

You have been provided with the following files:
1. `/home/user/auth_server/login_handler.cgi`: The compiled Linux ELF executable currently in production.
2. `/home/user/auth_server/login_handler.cpp`: The source code for the CGI binary. However, the secret key is defined in a separate compiled object file and is not visible in this source code.
3. `/home/user/new_key.txt`: A file containing the new secret key that must be used going forward.

Your objectives are:

**Phase 1: Binary Analysis & Vulnerability Demonstration**
1. Extract the old secret key from the compiled `login_handler.cgi` binary. The key is a 16-character alphanumeric string. Write this key exactly as it appears into `/home/user/old_key.txt`.
2. The CGI script expects a `QUERY_STRING` environment variable in the format `payload=<base64_url>&signature=<hex_hash>`. 
3. Generate a proof-of-concept (PoC) query string that exploits the open redirect vulnerability in the current binary to redirect a user to `http://attacker.com/steal`.
4. Save this exact query string (e.g., `payload=...&signature=...`) to `/home/user/exploit_qs.txt`.

**Phase 2: Code Remediation & Credential Rotation**
1. Copy `login_handler.cpp` to `/home/user/auth_server/login_handler_patched.cpp`.
2. Modify `login_handler_patched.cpp` to achieve the following:
   - Remove the `extern const char* SECRET_KEY;` declaration.
   - Hardcode the new secret key (read from `/home/user/new_key.txt`) directly into the code as a `const std::string SECRET_KEY`.
   - Fix the open redirect vulnerability. The patched code must ensure that the decoded `redirect_url` is a safe, relative path. Specifically, it MUST start with exactly one forward slash (`/`) and must NOT start with two forward slashes (`//`). If the URL does not meet these criteria, it should default the redirect URL to `/home`.
3. Compile your patched C++ code to `/home/user/auth_server/login_handler_patched.cgi` using `g++`.

Constraints:
- You must use standard C++11 or later.
- Do not use any external libraries outside the C++ standard library.
- The output in the `.txt` files must not contain trailing newlines or extra whitespace unless specified.