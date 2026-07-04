You are a security engineer tasked with rotating credentials and migrating a legacy authentication service. We have a stripped, legacy authentication binary located at `/app/legacy_auth`. We lost the source code, but we know it implements a custom token validation logic loosely similar to JWTs, but with some specific quirks and a hardcoded secret. 

Your objective is to reverse-engineer the `/app/legacy_auth` binary and write a BIT-EXACT equivalent Python script at `/home/user/auth_migrator.py`. 

The binary takes a single command-line argument containing the token string. 
Example invocation: `/app/legacy_auth "eyJhbGciOiAibWQ1In0=.eyB1c2VyIjogImFkbWluIiB9.signature"`

Your Python script must perfectly replicate the binary's behavior, including:
1. Parsing the custom token format (Base64Url encoded header, payload, and signature separated by dots).
2. Cryptographic hashing and checksum verification using the hardcoded secret found in the binary.
3. Handling any edge cases or vulnerabilities present in the binary's validation logic (e.g., how it handles missing signatures or specific algorithm headers).
4. Extracting and formatting the output exactly as the binary does, including redacting any sensitive data (like passwords) before printing the payload.
5. Emitting the exact same standard output and exit codes for valid tokens, invalid tokens, and malformed inputs.

Write your solution to `/home/user/auth_migrator.py`. It should take the token as `sys.argv[1]`.
We will run an automated fuzzer that passes thousands of randomly mutated tokens to both the legacy binary and your Python script to ensure their outputs and exit codes are identical.