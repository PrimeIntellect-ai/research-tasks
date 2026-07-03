You are a security engineer tasked with rotating credentials and securing a legacy authentication system. A proprietary token validation service was recently found to be vulnerable to signature bypass attacks (similar to the classic JWT `alg=none` vulnerability). The legacy token generator and validator is provided as a stripped binary at `/app/token_tool`. Unfortunately, the source code and the original HMAC secret key have been lost.

Your task is to implement a strict token filter in C++ that correctly validates these proprietary tokens, ensuring the vulnerability cannot be exploited, while still accepting valid tokens.

Here is what you know about the system:
- Tokens are provided in HTTP requests via the header: `Authorization: Bearer <token>`
- The token format is modeled after JWT: `Base64UrlEncode(Header) . Base64UrlEncode(Payload) . Base64UrlEncode(Signature)`
- The legacy `token_tool` uses HMAC-SHA256 to sign tokens. However, it incorrectly accepts tokens if the header specifies `{"alg": "none"}` or if the signature part is completely omitted.
- The secret key is hardcoded as a string inside the stripped binary `/app/token_tool`.

Your objectives:
1. Reverse-engineer or inspect `/app/token_tool` to recover the hardcoded HMAC-SHA256 secret key.
2. Write a C++ program at `/home/user/secure_filter.cpp` and compile it to the executable `/home/user/secure_filter`. You may use OpenSSL (`libssl` / `libcrypto`) for cryptographic functions.
3. Your compiled program must accept exactly one command-line argument: the path to a text file containing raw HTTP request headers.
4. Your program must parse the HTTP headers, extract the token, and strictly verify the HMAC-SHA256 signature using the recovered key.
5. Your program must reject any token that uses `alg: none`, lacks a valid signature, has a modified payload, or is malformed.
6. The program must print exactly `ACCEPT` (followed by a newline) to standard output if the token is valid and securely signed, and `REJECT` (followed by a newline) if it is invalid, missing, or malicious.

To help you develop and test your filter, we have provided two directories containing HTTP request files:
- `/app/corpus/clean/` contains perfectly valid requests. Your filter MUST accept 100% of these.
- `/app/corpus/evil/` contains malicious requests attempting to exploit the legacy bypass vulnerabilities. Your filter MUST reject 100% of these.

Ensure your compiled `/home/user/secure_filter` is ready for automated evaluation.