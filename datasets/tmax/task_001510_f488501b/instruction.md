You are a security auditor tasked with reviewing a custom authorization token library and implementing a detector for malicious tokens.

We have a vendored package for the library located at `/app/libsecauth-1.0`. The library is intended to parse a custom text-based token format, verify its cryptographic signature (using OpenSSL), and determine the user's role to enforce file access permissions. Recently, a critical privilege escalation vulnerability was reported—similar to the infamous "JWT alg=none" vulnerability—where specially crafted tokens can bypass signature verification.

Your objectives:
1. **Fix the Build System**: The vendored library at `/app/libsecauth-1.0` currently fails to build due to a deliberate perturbation in its `Makefile` (missing OpenSSL linkage). Fix the `Makefile` and run `make` to compile `libsecauth.so`.
2. **Audit and Patch**: Review the source code (specifically `token_parse.c` or related files). Identify the privilege escalation vulnerability that allows a token to bypass signature verification. Patch the library source code to reject these bypassed tokens.
3. **Build a Classifier**: Write a C program at `/home/user/detector.c` that includes the library's header (found in `/app/libsecauth-1.0/include/secauth.h`) and links against the fixed `libsecauth.so`.
   - The program must accept a single command-line argument: the path to a token file.
   - It should use the library's `secauth_validate_token(const char *filepath)` function.
   - If the function returns success (valid token), print exactly `ACCEPT` to standard output.
   - If the function returns failure (invalid, forged, or malicious token), print exactly `REJECT` to standard output.
   - Compile your program to `/home/user/detector`.

Ensure your `detector` correctly classifies the tokens. There is a corpus of tokens on the system that an automated verifier will use to test your program. Your program must correctly accept all clean tokens and reject all malicious ones.