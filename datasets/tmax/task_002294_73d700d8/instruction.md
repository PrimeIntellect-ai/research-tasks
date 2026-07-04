You are a forensics analyst investigating a compromised Linux host. The attacker managed to bypass authentication by exploiting a vulnerability in a custom authentication service that accepts JWTs with the "none" algorithm (`alg=none`). 

We have recovered the malicious token used by the attacker, located at `/home/user/evidence/token.jwt`. The payload of this token contains a custom claim called `exfil_path`, which points to a rogue TLS certificate that the attacker stashed inside an isolated, sandboxed environment on this machine.

Your task is to:
1. Write a C++ program at `/home/user/decoder.cpp` that parses the JWT token from `/home/user/evidence/token.jwt`. 
2. Your C++ program must implement Base64Url decoding to decode the header and the payload of the JWT. (Note: Base64Url is similar to standard Base64 but uses '-' instead of '+' and '_' instead of '/', and omits padding '=').
3. Extract the value of the `exfil_path` claim from the decoded JSON payload. You do not need a full JSON parsing library if you can reliably extract the string value manually.
4. Compile your program to `/home/user/decoder` and run it to discover the hidden path.
5. Once you have the path, inspect the rogue TLS certificate located at that path using standard Linux command-line tools.
6. Extract the SHA256 fingerprint of the rogue TLS certificate.
7. Save the SHA256 fingerprint exactly as outputted by OpenSSL (e.g., `SHA256 Fingerprint=AA:BB:CC:...`) into a log file at `/home/user/fingerprint.txt`.

Do not attempt to use external C++ libraries (like OpenSSL's libcrypto or nlohmann-json) in your C++ code; rely on standard C++ libraries (`<iostream>`, `<string>`, `<vector>`, etc.) to implement the Base64Url decoding and string searching.