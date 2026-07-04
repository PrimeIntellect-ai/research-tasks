You are an incident responder investigating a suspected breach of a custom web service. The web server uses a proprietary C-based CGI binary to validate session tokens. Reviewing the web logs, you suspect an attacker successfully bypassed the token validation to access the `/api/admin_panel` endpoint.

Your investigation environment is set up in `/home/user/`.

You have the following artifacts:
1. `/home/user/server.log` - The web server access logs containing HTTP requests, endpoints, and the Base64-encoded `token` parameters.
2. `/home/user/token_validator.c` - The source code for the vulnerable token validation program.

Perform the following tasks:
1. **Security Log Parsing & Decoding:** Analyze `/home/user/server.log` to identify the specific request where an attacker successfully accessed the `/api/admin_panel` endpoint (indicated by an HTTP 200 response). Extract the Base64-encoded token from this request, decode it, and save the raw binary decoded payload to `/home/user/decoded_payload.bin`.
2. **Vulnerability Remediation:** Analyze `/home/user/token_validator.c` to understand how the decoded payload exploited the token validation logic. 
3. **Secure Coding:** Create a fixed version of the C program and save it to `/home/user/token_validator_fixed.c`. 
   - Your fixed version must replace the unsafe string copy mechanism.
   - If the input token is exactly 32 bytes or longer (meaning it cannot safely fit inside a 32-byte buffer with a null terminator), the program MUST print exactly "Error: Token too long\n" to standard output and exit with status code 1.
   - Otherwise, the program should behave exactly as it originally did.
4. Compile your fixed C code to a binary located at `/home/user/token_validator_fixed` using `gcc`.

Ensure all files are precisely named and located in `/home/user/`.