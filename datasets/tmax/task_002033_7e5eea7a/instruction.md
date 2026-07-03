You are a security engineer responsible for rotating legacy cryptographic tokens for our internal data processing pipeline. Our old token generation system relies on a custom C-based Python extension called `libsectoken` which we are trying to modernize. 

Currently, the source code for the legacy package is vendored at `/app/vendored/libsectoken-1.2.0`. However, the previous maintainer made a mistake during a recent patch, and the package fails to build. 

Your tasks are as follows:

1. **Fix the Vendored Package:**
   Inspect the source code in `/app/vendored/libsectoken-1.2.0` and fix the compilation/build issue. The package uses a standard `setup.py`. Once fixed, install the package in the current environment.

2. **Reverse Engineer the Oracle:**
   We have an existing compiled binary oracle at `/app/oracle/token_oracle` that generates valid v2 tokens. You need to analyze this binary (using tools like `objdump`, `strings`, or `ltrace`) to understand how it constructs the new token payload from an input JSON string.

3. **Develop the Rotator Script:**
   Write a Python script at `/home/user/token_rotator.py` that takes a JSON string representing the token claims as a command-line argument. 
   The script must:
   - Use the fixed `libsectoken` library to generate a base cryptographic signature.
   - Embed a strict Content Security Policy (CSP) header string (`default-src 'none'; script-src 'self';`) inside the metadata block of the token format.
   - Output the exact same base64-encoded token string as the `/app/oracle/token_oracle` would for any given JSON input.

Your program's output must precisely match the output of `/app/oracle/token_oracle` for any valid input string. Your script should accept the input string as its first command-line argument and print *only* the resulting token to standard output.

Example invocation:
`python3 /home/user/token_rotator.py '{"user_id": 12345, "role": "admin"}'`