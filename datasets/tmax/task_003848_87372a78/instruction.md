You are a security auditor evaluating a proprietary authentication mechanism for a client's internal systems. 

You have been provided with the following artifacts:
1. `/app/auth_service`: A stripped Linux ELF binary that validates permission tokens. The binary takes three arguments: `./auth_service <username> <permission_level> <token>`. It returns exit code 0 if the token is valid for that user and permission, and exit code 1 otherwise.
2. `/home/user/client_stub.c`: A reference C implementation provided by the developers that supposedly generates valid tokens. However, the developers mentioned it "sometimes fails" and a recent automated scan flagged it for a security vulnerability.

Your objectives:
1. **Code Auditing & CWE Identification**: Review `/home/user/client_stub.c`. Identify the primary vulnerability class that causes the security flaw (e.g., Buffer Overflow, Predictable PRNG, Hardcoded Credentials). Write the exact CWE identifier (e.g., `CWE-123`) to `/home/user/cwe_flag.txt`.
2. **Reverse Engineering**: Analyze the `/app/auth_service` binary to understand the correct token generation logic. The token involves payload encoding and custom encryption/obfuscation.
3. **Secure Implementation**: Write a new C program at `/home/user/token_gen.c` that accurately and securely generates valid tokens. 
   - It must compile with `gcc /home/user/token_gen.c -o /home/user/token_gen`.
   - It must accept two arguments: `<username>` and `<permission_level>`.
   - It must output *only* the generated token to standard output.

An automated test will run your `token_gen` binary with 100 random username/permission pairs and pass the generated tokens to `/app/auth_service`. You must achieve a 100% success rate.